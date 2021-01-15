from decimal import Decimal
from contextlib import suppress
from django.urls import reverse
from django.utils import timezone
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _lazy
from common.models import UpdateModelMixin
from .managers import CitaManager
from . import utils


# TODO rename to TipoAgenda
class Agenda(models.Model):
    """Representa los tipos de agendas que maneja un cliente."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    duracion = models.DurationField(
        _lazy('duración'), help_text=_lazy('Duración de la atención para cada cita. Ingresar duración de la forma HH:MM:SS')
    )

    class Meta:
        verbose_name = 'agenda'
        verbose_name_plural = 'agendas'
    
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return '{}?tipo={}'.format(reverse('agenda:citas'), self.pk)

class DiagnosticoNotSet(Exception):
    pass

class Cita(UpdateModelMixin, models.Model):
    """Modelo para guardar las citas de un medico."""

    # Horario cita
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    medico = models.ForeignKey('organizacional.Empleado', related_name='citas')
    sucursal = models.ForeignKey('organizacional.Sucursal', related_name='citas')
    creada_el = models.DateTimeField(_lazy('fecha llamada'), auto_now_add=True)
    fecha_deseada = models.DateField(_lazy('fecha deseada'), blank=True, null=True)

    autorizacion = models.CharField(_lazy('autorización'), max_length=100, blank=True)
    autorizado_por = models.CharField(_lazy('autorizado por'), max_length=100, blank=True)
    fecha_autorizacion = models.DateField(_lazy('Fecha de autorización'), blank=True, null=True)
    formatos = models.ManyToManyField('historias.Formato', through='historias.Historia', related_name='citas')
    servicio_prestado = models.ForeignKey(
        'pacientes.ServicioRealizar', related_name='citas', verbose_name=_lazy('servicio prestado')
    )
    detalle_factura = models.ForeignKey(
        'facturacion.DetalleFactura', on_delete=models.SET_NULL, related_name='citas', blank=True, null=True,
    )

    objects = CitaManager()

    class Meta:
        verbose_name = 'cita'
        verbose_name_plural = 'citas'
        ordering = ['inicio']
        permissions = [
            ('puede_ver_agenda', 'Puede ver la agenda'),
            ('can_agendar_citas', 'Puede agendar citas'),
            ('can_see_todas_citas', 'Puede ver todas las citas'),
            ('puede_ver_todas_citas', 'Puede ver todas las citas'),
            ('can_see_agenda_diaria', 'Puede ver la agenda diaria'),
            ('puede_cambiar_estado', 'Puede cambiar el estado de una cita'),
            ('can_generar_indicadores_resolucion_256', 'Puede generar reporte para los indicadores para la resolucion 256'),
            ('can_set_cumplida_dia_diferente', 'Puede cambiar el estado a cumplida sin que la fecha de la cita sea el dia actual'),
        ]
    
    def __str__(self):
        return '{} - {}'.format(self.id, self.paciente)

    @property
    def duracion(self):
        return self.fin - self.inicio

    @property
    def paciente(self):
        """Paciente asociado a la cita."""

        return self.servicio_prestado.paciente
    
    @property
    def servicio(self):
        """Servicio prestado en la cita."""

        return self.servicio_prestado.servicio
    
    @property
    def empresa(self):
        """Convenio usado por el paciente en la cita."""

        return self.servicio_prestado.convenio
    
    @property
    def institucion(self):
        """IPS que factura la cita."""

        return self.servicio_prestado.orden.institucion

    @property
    def start(self):
        return self.inicio

    @property
    def end(self):
        return self.fin
    
    @property
    def color(self):
        return self.historial_actual.color

    @property
    def cumplida(self):
        return self.estado_actual == self.estados.model.CUMPLIDA
    
    @property
    def terminada(self):
        return self.estado_actual == self.estados.model.TERMINADA
    
    @property
    def cancelada(self):
        return self.estado_actual == self.estados.model.CANCELADA

    @property
    def estado_actual(self):
        """Devuelve el estado actual de la cita."""

        estado = getattr(self, 'state', None)
        return estado or getattr(self.historial_actual, 'estado', None)
    
    @property
    def estado_display(self):
        """Devuelve el nombre de estado actual de la cita."""

        ESTADOS = self.estados.model.ESTADOS
        return list(filter(lambda o: o[0] == self.estado_actual, ESTADOS))[0][1]
    
    @property
    def historial_actual(self):
        """Retorna el historial del estado actual"""

        return self.estados.first()
    
    @property
    def diagnostico(self):
        """Retorna el diagnostico asociado a la cita."""

        try:
            return next(filter(lambda e: e.formato.diagnostico, self.encuentros.all())).diagnostico
        except:
            raise DiagnosticoNotSet
    
    @property
    def factura(self):
        """Retorna la factura."""

        with suppress(Exception):
            return self.detalle_factura.factura
        
        return None

    @property
    def can_move(self):
        """Indica si la cita se puede mover a otro horario."""

        model = self.estados.model
        return self.estado_actual in [model.NO_CONFIRMADA, model.CONFIRMADA, model.CUMPLIDA]
    
    @property
    def valor_pagar_medico(self):
        """Valo a pagar a medico."""

        return self.servicio_prestado.valor_pagar_medico(self.medico)

    def can_add_encuentro(self, user):
        """Indica si se puede agregar encuentro a la cita."""

        if user.has_perm('historias.puede_editar_historias'):
            return True
        
        return not self.terminada

    def can_set_cumplida(self, user):
        """Indica si se puede cambiar el estado de la cita a cumplida."""

        if user.has_perm('agenda.can_set_cumplida_dia_diferente'):
            return True

        now = timezone.localtime(timezone.now())
        start = timezone.localtime(self.start)

        return start.date() == now.date()
    
    def estados_disponibles(self, user):
        """Devuelve una lista con los estados que puede tener la cita."""
        
        Estado = self.estados.model
        DISPONIBILIDAD_ESTADOS = {
            Estado.NO_CONFIRMADA: [Estado.CONFIRMADA, Estado.CUMPLIDA, Estado.NO_ASISTIO, Estado.EXCUSADA, Estado.CANCELADA],
            Estado.CONFIRMADA: [Estado.CUMPLIDA, Estado.NO_ASISTIO, Estado.EXCUSADA, Estado.CANCELADA],
            Estado.CUMPLIDA: [Estado.NO_ATENDIDA, Estado.CANCELADA],
            Estado.NO_ATENDIDA: [Estado.CANCELADA, Estado.CONFIRMADA],
            Estado.NO_ASISTIO: [Estado.CONFIRMADA],
            Estado.EXCUSADA: [Estado.CONFIRMADA],
        }

        if self.estado_actual not in DISPONIBILIDAD_ESTADOS:
            return []
        
        disponibles = DISPONIBILIDAD_ESTADOS[self.estado_actual]
        if Estado.CUMPLIDA in disponibles and not self.can_set_cumplida(user):
            disponibles.remove(Estado.CUMPLIDA)
        
        if self.estado_actual in [Estado.NO_ASISTIO, Estado.NO_ATENDIDA, Estado.EXCUSADA] and not self.can_edit(user):
            disponibles.remove(Estado.CONFIRMADA)
        
        return disponibles
    
    # permisos
    def can_change_estado(self, user):
        """Indica si el usuario puede cambiar el estado a la cita."""

        return user.has_perm('agenda.puede_cambiar_estado')

    def can_edit(self, user):
        """Indica si la cita puede ser editada."""

        if user.has_perm('pacientes.can_edit_orden'):
            return True
        
        return self.can_move
    
    def orden_url(self, user):
        """URL de la orden."""

        Estado = self.estados.model
        if user.has_perm('pacientes.puede_ver_orden_sin_paciente') or (
            user.has_perm('pacientes.puede_ver_orden') and self.estado_actual not in [
                Estado.NO_CONFIRMADA, Estado.CONFIRMADA
        ]):
            return reverse('pacientes:ordenes-detalle', kwargs={'pk': self.servicio_prestado.orden_id})
        return None
    
    def visita_url(self, user):
        if user.has_perm('historias.can_add_historia_escaneada'):
            return reverse('pacientes:historias-sesion', kwargs={'pk': self.id})

        Estado = self.estados.model
        ver_visita = self.estado_actual in [
            Estado.CUMPLIDA,
            Estado.EXCUSADA,
            Estado.TERMINADA,
            Estado.CANCELADA,
            Estado.NO_ASISTIO,
            Estado.NO_ATENDIDA
        ]

        con_orden = self.servicio_prestado.orden.paciente.fecha_ingreso
        if user.has_perm('historias.add_historia') and ver_visita and con_orden:
            return reverse('pacientes:historias-sesion', kwargs={'pk': self.id})

        return None
    
    def redirecciona_url(self):
        if not self.paciente.fecha_ingreso:
            return '{}?cita={}'.format(reverse('pacientes:detalle', kwargs={'pk': self.paciente.id}), self.id)
        
        return reverse('pacientes:ordenes-detalle', kwargs={'pk': self.servicio_prestado.orden_id})

    @transaction.atomic
    def actualizar_estado(self, estado, empleado, motivo='', reagendar=False):
        """Crea nuevo estado en el historial de estados."""

        HistorialEstado = self.estados.model
        if self.estado_actual != estado:
            HistorialEstado.objects.create(estado=estado, empleado=empleado, motivo=motivo, cita=self)

            if estado == HistorialEstado.TERMINADA:
                self.servicio_prestado.cambiar_estado()
            if estado == HistorialEstado.CANCELADA and self.servicio_prestado:
                estados = [HistorialEstado.CUMPLIDA, HistorialEstado.NO_CONFIRMADA, HistorialEstado.CONFIRMADA]
                estados_cancelados = [
                    HistorialEstado(estado=HistorialEstado.CANCELADA, empleado=empleado, motivo=motivo, cita=cita)
                    for cita in self.servicio_prestado.citas.filter(inicio__gt=self.inicio).by_estados(estados)
                ]
                HistorialEstado.objects.bulk_create(estados_cancelados)
                self.servicio_prestado.cancelar()
            if reagendar:
                self.servicio_prestado.reagendar_citas(empleado, cantidad=1)

    def terminar_cita(self, empleado):
        """Marca la cita como terminada."""

        if self.estado_actual != self.estados.model.CANCELADA:
            self.actualizar_estado(self.estados.model.TERMINADA, empleado)

    @transaction.atomic
    def mover_cita(self, **kwargs):
        """"Mueve la cita a un nuevo horario"""

        duracion = self.duracion
        for field, value in kwargs.items():
            setattr(self, field, value)

        self.fin = utils.fin_cita(self.inicio, duracion)
        self.save()
        return self

class HistorialEstado(models.Model):
    """Guarda el historial de los estados de una cita."""

    CUMPLIDA = 'CU'
    EXCUSADA = 'EX'
    CANCELADA = 'CA'
    TERMINADA = 'TE'
    CONFIRMADA = 'CO'
    NO_ASISTIO = 'NA'
    NO_ATENDIDA = 'NT'
    NO_CONFIRMADA = 'NC'
    ESTADOS = (
        (NO_CONFIRMADA, _lazy('No confirmada')),
        (CONFIRMADA, _lazy('Confirmada')),
        (CUMPLIDA, _lazy('Cumplida')),
        (TERMINADA, _lazy('Atendida')),
        (NO_ATENDIDA, _lazy('No atendida')),
        (CANCELADA, _lazy('Cancelada')),
        (EXCUSADA, _lazy('Excusada')),
        (NO_ASISTIO, _lazy('No asistio')),
    )

    cita = models.ForeignKey(Cita, related_name='estados', verbose_name=_lazy('cita'))
    empleado = models.ForeignKey('organizacional.Empleado', related_name='estados')
    estado = models.CharField(_lazy('estado'), max_length=2, choices=ESTADOS)
    fecha = models.DateTimeField(_lazy('fecha'), auto_now_add=True)
    motivo = models.TextField(_lazy('motivo'), blank=True)

    class Meta:
        verbose_name = 'historial estado'
        verbose_name_plural = 'historial estados'
        ordering = ['-fecha']
    
    def __str__(self):
        return '{} - {} - {}'.format(self.cita_id, self.estado, self.fecha)

    @property
    def estado_display(self):
        """Devuelve el nombre de estado actual de la cita."""

        return list(filter(lambda o: o[0] == self.estado, self.ESTADOS))[0][1]
    
    @property
    def color(self):

        _colors = {
            self.EXCUSADA: 'gray',
            self.CANCELADA: 'blue',
            self.CUMPLIDA: 'green',
            self.NO_ATENDIDA: 'pink',
            self.NO_ASISTIO: 'purple',
            self.NO_CONFIRMADA: 'red',
            self.CONFIRMADA: 'yellow',
            self.TERMINADA: 'lightgreen',
        }

        return _colors[self.estado]
