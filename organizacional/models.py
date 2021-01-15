import warnings
import itertools
from django.conf import settings
from django.utils import timezone
from datetime import date, datetime
from django.db import models, transaction
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _lazy
from . import managers

class Sucursal(models.Model):
    """Modelo para guardar las sucursales de los clientes."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    direccion = models.CharField(_lazy('dirección'), max_length=100, blank=True)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)
    codigo_contable_recibo = models.PositiveIntegerField(blank=True, null=True, help_text='Usado en la exportación de recibos de caja')

    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'
    
    def __str__(self):
        return self.nombre


def logo_institucion_path(instance, filename):
    return 'institucion_{0}/logo_{1}'.format(instance.pk, filename)

class Institucion(models.Model):
    """Modelo para guardar las instituciones que facturan."""


    NIT = 'NI'
    PASAPORTE = 'PA'
    CEDULA_CIUDADANIA = 'CC'
    CEDULA_EXTRANJERIA = 'CE'
    TIPO_DOCUMENTOS = (
        (NIT, _lazy('NIT')),
        (CEDULA_CIUDADANIA, _lazy('Cédula de ciudadanía')),
        (CEDULA_EXTRANJERIA, _lazy('Cédula de extranjería')),
        (PASAPORTE, _lazy('Pasaporte'))
    )

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    razon_social = models.CharField(_lazy('razón social'), max_length=100)
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    identificacion = models.CharField(_lazy('identificación'), max_length=50, unique=True)
    codigo = models.CharField(_lazy('código'), max_length=50, blank=True)
    direccion = models.CharField(_lazy('dirección'), max_length=100)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)
    ciudad = models.ForeignKey('globales.Poblado', related_name='instituciones', verbose_name=_lazy('ciudad'))
    logo = models.ImageField(upload_to=logo_institucion_path ,verbose_name=_lazy('logo'), blank=True)

    # Historia params
    titulo_historia = models.CharField(_lazy('titulo en historia'), max_length=100)
    universidad = models.CharField(_lazy('universidad historia'), max_length=100, blank=True)
    subtitulo_historia = models.CharField(_lazy('subtitulo en historia'), max_length=100, blank=True)
    
    # Facturacion
    firma_factura = models.ForeignKey('organizacional.Empleado', related_name='instituciones_firmo', blank=True, null=True)
    footer_factura = models.CharField(max_length=100, default='representante legal')

    class Meta:
        verbose_name = 'institución'
        verbose_name_plural = 'instituciones'

    def __str__(self):
        return self.nombre
    
    def consecutivo_factura(self):
        """Retorna el nombre del consecutivo de la factura para la institución."""

        return 'factura_{}'.format(self.id)
    
    def nit_sin_digito_verificacion(self):
        """Retorna el nit sin digito de verificacion."""

        return self.identificacion.split('-')[0]

class SinHorarioAtencion(Exception):
    pass

def empleado_firma_path(instance, filename):
    return 'empleado_{0}/firma_{1}'.format(instance.pk, filename)

class Empleado(models.Model):
    """Modelo para guardar los empleados de un cliente."""

    MEDICO = 'M'
    ADMINISTRATIVO = 'A'
    TIPOS = (
        (MEDICO, _lazy('medico')),
        (ADMINISTRATIVO, 'administrativo')
    )

    nombres = models.CharField(_lazy('nombres'), max_length=100)
    apellidos = models.CharField(_lazy('apellidos'), max_length=100)
    cedula = models.PositiveIntegerField(_lazy('cédula'))
    activo = models.BooleanField(_lazy('activo'), default=True)
    registro_medico = models.CharField(_lazy('registro medico'), max_length=100, blank=True)
    firma = models.ImageField(upload_to=empleado_firma_path ,verbose_name=_lazy('firma'), blank=True)
    tipo = models.CharField(_lazy('tipo'), max_length=2, choices=TIPOS, default=ADMINISTRATIVO)
    instituciones = models.ManyToManyField(Institucion, related_name='empleados', verbose_name=_lazy('instituciones'))
    duracion_cita = models.DurationField(
        _lazy('duración de las citas'), null=True, blank=True, help_text=_lazy('Ingresar duración de la forma HH:MM:SS')
    )
    agenda = models.ForeignKey('agenda.Agenda', related_name='empleados', verbose_name=_lazy('agenda'), blank=True, null=True)
    porcentaje_pago = models.PositiveIntegerField(
        _lazy('porcentaje de pago'), validators=[MaxValueValidator(100)], default=0
    )
    atenciones_simultaneas = models.PositiveIntegerField(
        _lazy('atenciones simulataneas'), blank=True, null=True, help_text=_lazy('Pacientes que puede atender al mismo tiempo')
    )
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_lazy('usuario'))

    # Historia params
    especialidad_historia = models.CharField(_lazy('especialidad historia'), max_length=100, blank=True)

    # Managers
    objects = managers.EmpleadoManager()
    username = None  # For use in import_export

    class Meta:
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'
        permissions = [
            ('can_add_empleado', 'Puede agregar empleados'),
            ('can_ingresar_sin_restriccion', 'Puede ingresar sin ninguna restriccion'),
        ]
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    @property
    def duracion(self):
        """Duración de la atención de las citas"""

        return self.duracion_cita or self.agenda.duracion
    
    @property
    def sucursales(self):
        """Sucursales en las cuales atiende el medico."""

        return Sucursal.objects.filter(id__in=self.horarios_atencion.values_list('sucursal'))
    
    @property
    def turnos(self):
        warnings.warn('Usar atenciones_simultaneas')
        return self.atenciones_simultaneas

    def horas_atencion(self, fechas, sucursal):
        def cantidad_citas_hora(hora, citas):
            i = 0
            total = 0
            while i < len(citas) and hora >= timezone.localtime(citas[i].inicio).time():
                if timezone.localtime(citas[i].inicio).time() <= hora < timezone.localtime(citas[i].fin).time():
                    total = total + 1
                i = i + 1

            return hora, total
        
        if not isinstance(fechas, list):
            warnings.warn('Debe ser una lista de fechas')
            fechas = [fechas]
        
        horarios = self.horarios_atencion.by_sucursal(sucursal)
        if not horarios.exists():
            raise SinHorarioAtencion('{} no tiene horarios de atencion en la sucursal {}'.format(self, sucursal))

        horarios = self.horarios_atencion.by_sucursal(sucursal).by_fechas(fechas)
        horas_dia = {h.dia: h.espacios_atencion() for h in horarios}
        horas_fecha = {f: horas_dia.get(str(f.weekday() + 1), []) for f in fechas}

        if self.atenciones_simultaneas:
            citas = self.citas.aceptadas().by_sucursal(sucursal).by_fechas(fechas)
            
            result = {}
            for f in fechas:
                citas_fecha = list(filter(lambda cita: cita.inicio.date() == f, citas))
                citas_agrupadas = dict(map(lambda h: cantidad_citas_hora(h, citas_fecha), horas_fecha[f]))
                result[f] = list(filter(lambda h: citas_agrupadas.get(h, 0) < self.atenciones_simultaneas, horas_fecha[f]))
            
            return result
                
        return horas_fecha

    @transaction.atomic
    def guardar_horarios(self, sucursal, horarios):
        HorarioAtencion = self.horarios_atencion.model
        updated = []
        for horario in horarios:
            if not horario.get('con_descanso', False):
                horario.update({'con_descanso': False, 'inicio_descanso': None, 'fin_descanso': None})
            obj, _ = HorarioAtencion.objects.update_or_create(
                medico=self, dia=horario['dia'], sucursal=sucursal,
                defaults=horario
            )
            updated.append(obj.id)

        self.horarios_atencion.filter(sucursal=sucursal).exclude(id__in=updated).delete()
    
    @transaction.atomic
    def update(self, username, password, rol, **kwargs):
        """Actualiza los datos del empleado."""

        self.usuario.groups.set([rol])
        if username != self.usuario.username:
            self.usuario.username = username
        
        if password:
            self.usuario.set_password(password)
        
        self.usuario.save()

        for field, value in kwargs.items():
            setattr(self, field, value)

        self.save()

class HorarioAtencion(models.Model):
    """Horario de atención de medicos."""

    LUNES = '1'
    MARTES = '2'
    MIERCOLES = '3'
    JUEVES = '4'
    VIERNES = '5'
    SABADO = '6'
    DOMINGO = '7'
    DIAS = (
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miercoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sabado'),
        (DOMINGO, 'Domingo'),
    )

    fin = models.TimeField()
    inicio = models.TimeField()
    dia = models.CharField(max_length=2, choices=DIAS)
    con_descanso = models.BooleanField(default=False)
    fin_descanso = models.TimeField(blank=True, null=True)
    inicio_descanso = models.TimeField(blank=True, null=True)
    medico = models.ForeignKey(Empleado, related_name='horarios_atencion')
    sucursal = models.ForeignKey(Sucursal, related_name='horarios_atencion')

    # Managers
    objects = managers.HorarioAtencionManager()

    class Meta:
        verbose_name = 'horario de atención'
        verbose_name_plural = 'horarios de atención'
        permissions = [
            ('can_add_horario_atencion', 'Puede guardar el horario de atencion de los medicos'),
        ]
    
    def __str__(self):
        return '{} - {} - ({} - {})'.format(self.medico, self.get_dia_display(), self.inicio, self.fin)
    
    def espacios_atencion(self):
        """Devuelve las horas especificas de atención segun la duracion de la atención del medico."""

        if not self.medico.activo:
            return []

        duracion = self.medico.duracion
        if self.con_descanso:
            espacios = self._get_espacios(self.inicio, self.inicio_descanso, duracion)
            espacios.extend(self._get_espacios(self.fin_descanso, self.fin, duracion))
            return espacios

        return self._get_espacios(self.inicio, self.fin, duracion)
    
    def _get_espacios(self, inicio, fin, duracion):
        """Retorna una lista con espacios(horas) de atención disponibles."""

        espacios = []
        actual = inicio
        while actual < fin:
            espacios.append(actual)
            actual = (datetime.combine(date.today(), actual) + duracion).time()

        return espacios
