import warnings
from datetime import datetime, date, timedelta
from django.utils.module_loading import import_string
from django.db.models import OuterRef, Subquery, Q
from django.db import models, transaction
from . import utils

ORDEN_PATH = 'pacientes.models.Orden'
SERVICIO_PATH = 'servicios.models.Servicio'
PACIENTE_PATH = 'pacientes.models.Paciente'
HISTORIAL_ESTADO_PATH = 'agenda.models.HistorialEstado'
SERVICIO_REALIZAR_PATH = 'pacientes.models.ServicioRealizar'

def HistorialEstadoModel():
        """
        :returns:
            Modelo de HistorialEstado.
        """

        return import_string('agenda.models.HistorialEstado')

class CitaQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Cita."""

    def fecha_entre(self, desde=None, hasta=None):
        """
        Filtra las citas con fecha entre el rango ingresado.
        """

        citas = self
        if desde:
            citas = citas.filter(inicio__date__gte=desde)
        
        if hasta:
            citas = citas.filter(inicio__date__lte=hasta)
        return citas

    def by_fecha(self, fecha):
        """Filtra las citas por fecha.
        
        :param date fecha: Fecha de las citas.
        """

        return self.filter(inicio__date=fecha)

    def by_fechas(self, fechas):
        """Filtra las citas por fechas.
        
        :param list fechas: Lista de fechas de las citas.
        """

        return self.filter(inicio__date__in=fechas)
    
    def by_medico(self, medico):
        """Filtra las citas por medico.
        
        :param medico: Medico que atendio las citas.
        """

        return self.filter(medico=medico)

    def by_institucion(self, institucion):
        """Filtra las citas por institucion.
        
        :param institucion: Institucion que atendio las citas.
        """

        return self.filter(servicio_prestado__orden__institucion=institucion)

    def by_sucursal(self, sucursal):
        """Filtra las citas por sucursal.
        
        :param sucursal: Sucursal donde se atendieron las citas.
        """

        return self.filter(sucursal=sucursal)

    def by_user(self, user):
        """
        Filtra las citas según las citas del usuario ingresado.

        :param user: Usuario.
        """

        if user.has_perm('agenda.puede_ver_todas_citas'):
            return self.all()
        
        return self.filter(medico__usuario=user)

    def annotate_estado(self):
        """Annotates la cita con el ultimo estado ingresado."""

        latest_estado = HistorialEstadoModel().objects.filter(cita=OuterRef('id')).values('estado')[:1]
        return self.annotate(state=Subquery(latest_estado))
    
    def atendidas(self):
        """Un queryset con las citas que fueron atendidas."""

        return self.annotate_estado().filter(state=HistorialEstadoModel().TERMINADA)
    
    def no_atendidas(self):
        """Un queryset con las citas que no han sido atendidas."""

        return self.annotate_estado().exclude(state=HistorialEstadoModel().TERMINADA)
    
    def canceladas(self):
        """Un queryset con las citas que fueron canceladas."""

        return self.annotate_estado().filter(state=HistorialEstadoModel().CANCELADA)

    def no_cumplidas(self):
        """Un queryset con las citas que no se cumplieron."""

        HistorialEstado = HistorialEstadoModel()
        return self.by_estados([
            HistorialEstado.EXCUSADA,
            HistorialEstado.CANCELADA,
            HistorialEstado.NO_ASISTIO,
            HistorialEstado.NO_ATENDIDA,
        ])
    
    def aceptadas(self):
        """Un queryset con las citas no_confirmadas, confirmadas, cumplidas y atendidas."""

        HistorialEstado = HistorialEstadoModel()
        return self.by_estados([
            HistorialEstado.CUMPLIDA,
            HistorialEstado.TERMINADA,
            HistorialEstado.CONFIRMADA,
            HistorialEstado.NO_CONFIRMADA,
        ])

    def by_estados(self, estados):
        """
        Filtra las citas que en su estado actual tenga algunos de los estados ingresados.

        :param list estados:
        """

        return self.annotate_estado().filter(state__in=estados)
    
    def exclude_by_estados(self, estados):
        """Excluye las citas que en su estado actual tenga los estados ingresados.
        
        :param list estados:
        """

        return self.annotate_estado().exclude(state__in=estados)
    
    def facturadas(self):
        """Un queryset con las citas que han sido facturadas."""

        return self.filter(detalle_factura__isnull=False)
    
    def no_facturadas(self):
        """Un queryset con las citas que no han sido facturadas."""

        return self.filter(detalle_factura__isnull=True)
    
    def paciente_creado(self, desde, hasta):
        """
        Un queryset con las citas creadas en rango de fechas escogido de los pacientes creados
        en el mismo rango de fechas.
        """

        return self.filter(servicio_prestado__orden__paciente__creado_el__range=(desde, hasta), creada_el__range=(desde, hasta))
    
    def primera_vez(self, desde, hasta):
        """Un queryset con las citas de primera vez dentro del rango de fechas escogido."""

        Paciente = import_string(PACIENTE_PATH)
        pacientes = (
            Paciente.objects
                .filter(creado_el__range=(desde, hasta))
                .annotate(primera_cita=Subquery(
                    self.model.objects.filter(paciente=OuterRef('pk')).values('pk')[:1]
                ))
        )
        return self.filter(id__in=pacientes.values('primera_cita'))

    def facturas(self, facturas):
        """Un queryset con las citas filtradas por facturas."""

        return self.filter(detalle_factura__factura__in=facturas)
    
    def consultas(self):
        """Un queryset con las citas que atienden consultas."""

        Servicio = import_string(SERVICIO_PATH)
        return self.filter(servicio_prestado__servicio__in=Servicio.objects.consultas())
    
    def procedimientos(self):
        """Un queryset con las citas que atienden procedimientos."""

        Servicio = import_string(SERVICIO_PATH)
        return self.filter(servicio_prestado__servicio__in=Servicio.objects.procedimientos())
    
    def not_otros(self):
        """Un queryset con las citas que no atienden otros."""

        Servicio = import_string(SERVICIO_PATH)
        return self.exclude(servicio_prestado__servicio__in=Servicio.objects.not_otros())

    def auditados_fin_tratamiento(self):
        """Retorna las citas que ya han sido verificadas."""

        return self.filter(servicio_prestado__verificado_por__isnull=False)

    def auditados_fin_tratamiento_entre(self, desde, hasta):
        """Retorna las citas verificadas entre el rango de fecha escogida."""
        
        return self.filter(servicio_prestado__verificado_at__range=(desde, hasta))

    def disponibles_facturar(self):
        """Retorna las citas disponibles a facturar"""

        return self.atendidas().no_facturadas().filter(servicio_prestado__verificado_por__isnull=False)

class CitaManager(models.Manager.from_queryset(CitaQuerySet)):
    """Manager personalizado para el modelo Cita."""

    @transaction.atomic
    def agendar(self, paciente_data, estado, empleado, institucion, servicio, convenio, medico, inicio, duracion, **kwargs):
        """Agenda una nueva cita."""

        warnings.warn('Usar metodo agendar_cita en services')
        agendar_cita = import_string('agenda.services.agendar_cita')
        return agendar_cita(paciente_data, estado, empleado, institucion, servicio, convenio, medico, inicio, duracion, **kwargs)

    @transaction.atomic
    def agendamiento_multiple_futuro(self, cantidad, desde, hora, duracion, medico, sucursal, servicio_prestado, empleado, aut='', fecha_aut=None):
        """Permite agendar multiples citas a partir de una fecha (incluyente) especifica.
        
        :param Date desde: Fecha a partir de la cual se van a agendar las citas.
        :returns: Lista con las nuevas citas agendadas.
        """

        warnings.warn('Usar agendar_multiples_citas en services')
        agendar_multiples_citas = import_string('agenda.services.agendar_multiples_citas')
        return agendar_multiples_citas(cantidad, desde, hora, duracion, medico, sucursal, servicio_prestado, empleado, aut, fecha_aut)
    

    @transaction.atomic
    def agregar_autorizacion(self, cita, autorizacion, fecha_autorizacion, autorizado_por=''):
        """Permite editar la autorizacion a la cita ingresada."""

        warnings.warn('Usar agregar_autorizacion en services')
        agregar_autorizacion = import_string('agenda.services.agregar_autorizacion')
        agregar_autorizacion(cita, autorizacion, fecha_autorizacion, autorizado_por)
    
    def autorizacion_automatica(self, cita):
        """Permite agregar autorizacion a ordenes de clientes que no requieren autorizacion."""

        agregar_autorizacion = import_string('agenda.services.agregar_autorizacion')

        orden = cita.servicio_prestado.orden
        agregar_autorizacion(cita, 'AU{}'.format(orden.id), orden.fecha_orden)
