import math
import warnings
import datetime
from contextlib import suppress
from decimal import Decimal, getcontext
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _lazy
from rest_framework.reverse import reverse
from common.models import UpdateModelMixin
from agenda.utils import fin_cita
from .managers import PacienteManager, ServicioRealizarManager

CITA_PATH = 'agenda.models.Cita'
HISTORIAL_ESTADO_PATH = 'agenda.models.HistorialEstado'
HORARIO_ATENCION_PATH = 'organizacional.models.HorarioAtencion'

class ParentescoMixin(object):
    """Mixin para los parentescos de un paciente."""

    TIO = 'T'
    OTRO = 'O'
    HIJO = 'I'
    PADRE = 'P'
    MADRE = 'M'
    AMIGO = 'AM'
    ABUELO = 'A'
    PRIMO = 'PR'
    HERMANO = 'H'
    CONYUGUE = 'C'
    PARENTESCOS = (
        (PADRE, _lazy('Padre')),
        (MADRE, _lazy('Madre')),
        (HERMANO, _lazy('Hermano')),
        (HIJO, _lazy('Hijo')),
        (ABUELO, _lazy('Abuelo')),
        (TIO, _lazy('Tio')),
        (PRIMO, _lazy('Primo')),
        (CONYUGUE, _lazy('Conyugue')),
        (AMIGO, _lazy('Amigo')),
        (OTRO, _lazy('Otro'))
    )

def paciente_foto_path(instance, filename):
    """Path para la foto de un paciente."""

    return 'paciente_{0}/foto_{1}'.format(instance.numero_documento, filename)

def paciente_firma_path(instance, filename):
    """Path para la firma de un paciente."""

    return 'paciente_{0}/firma_{1}'.format(instance.numero_documento, filename)

class Paciente(UpdateModelMixin, models.Model):
    """Modelo para guardar la información de un paciente."""

    FEMENINO = 'F'
    MASCULINO = 'M'
    GENEROS = (
        (FEMENINO, _lazy('Femenino')),
        (MASCULINO, _lazy('Masculino'))
    )

    MENOR_NN = 'MN'
    ADULTO_NN = 'AN'
    PASAPORTE = 'PA'
    REGISTRO_CIVIL = 'RC'
    NUMERO_UNICO_ID = 'NU'
    CEDULA_CIUDADANIA = 'CC'
    TARJETA_IDENTIDAD = 'TI'
    CEDULA_EXTRANJERIA = 'CE'
    CARNET_DIPLOMATICO = 'CD'
    TIPO_DOCUMENTOS = (
        (CEDULA_CIUDADANIA, _lazy('Cédula de ciudadanía')),
        (CEDULA_EXTRANJERIA, _lazy('Cédula de extranjería')),
        (PASAPORTE, _lazy('Pasaporte')),
        (REGISTRO_CIVIL, _lazy('Registro civil')),
        (TARJETA_IDENTIDAD, _lazy('Tarjeta de identidad')),
        (CARNET_DIPLOMATICO, _lazy('Carnet diplomatico')),
        (ADULTO_NN, _lazy('Adulto sin identificar')),
        (MENOR_NN, _lazy('Menor sin identificar')),
        (NUMERO_UNICO_ID, 'Número único de identificación')
    )

    VIUDO = 'V'
    CASADO = 'C'
    SOLTERO = 'S'
    DIVORCIADO = 'D'
    UNION_LIBRE = 'UL'
    ESTADOS_CIVILES = (
        (VIUDO, _lazy('Viudo')),
        (CASADO, _lazy('Casado')),
        (SOLTERO, _lazy('Soltero')),
        (DIVORCIADO, _lazy('Divociado')),
        (UNION_LIBRE, _lazy('Unión libre'))
    )

    RURAL = 'R'
    URBANO = 'U'
    ZONAS = (
        (URBANO, _lazy('Urbano')),
        (RURAL, _lazy('Rural'))
    )

    O_POSITIVO = 'O+'
    O_NEGATIVO = 'O-'
    A_POSITIVO = 'A+'
    A_NEGATIVO = 'A-'
    B_POSITIVO = 'B+'
    B_NEGATIVO = 'B-'
    AB_POSITIVO = 'AB+'
    AB_NEGATIVO = 'AB-'
    GRUPOS_SANGUINEOS = (
        (O_NEGATIVO, O_NEGATIVO),
        (O_POSITIVO, O_POSITIVO),
        (A_NEGATIVO, A_NEGATIVO),
        (A_POSITIVO, A_POSITIVO),
        (B_NEGATIVO, B_NEGATIVO),
        (B_POSITIVO, B_POSITIVO),
        (AB_NEGATIVO, AB_NEGATIVO),
        (AB_POSITIVO, AB_POSITIVO),
    )

    OTRO = 'O'
    NEGRO = 'N'
    INDIGENA = 'I'
    DESPLAZADO = 'D'
    GRUPOS_ETNICOS = (
        (DESPLAZADO, _lazy('Desplazado')),
        (INDIGENA, _lazy('Indigena')),
        (NEGRO, _lazy('Negro')),
        (OTRO, _lazy('Otro'))
    )

    MEDICO = 'ME'
    AMIGOS = 'AM'
    REFERIDO = 'R'
    INTERNET = 'IN'
    FACEBOOK = 'FB'
    PACIENTE = 'PA'
    INSTAGRAM = 'IG'
    PROCEDENCIAS = (
        (MEDICO, _lazy('Medico')),
        (AMIGOS, _lazy('Amigos')),
        (PACIENTE, _lazy('Paciente')),
        (INSTAGRAM, _lazy('Instagram')),
        (FACEBOOK, _lazy('Facebook')),
        (INTERNET, _lazy('Internet')),
        (REFERIDO, _lazy('Referido'))
    )

    TIO = 'T'
    OTRO = 'O'
    HIJO = 'I'
    PADRE = 'P'
    MADRE = 'M'
    AMIGO = 'AM'
    ABUELO = 'A'
    PRIMO = 'PR'
    HERMANO = 'H'
    CONYUGUE = 'C'
    PARENTESCOS = (
        (PADRE, _lazy('Padre')),
        (MADRE, _lazy('Madre')),
        (HERMANO, _lazy('Hermano')),
        (HIJO, _lazy('Hijo')),
        (ABUELO, _lazy('Abuelo')),
        (TIO, _lazy('Tio')),
        (PRIMO, _lazy('Primo')),
        (CONYUGUE, _lazy('Conyugue')),
        (AMIGO, _lazy('Amigo')),
        (OTRO, _lazy('Otro'))
    )

    primer_nombre = models.CharField(_lazy('primer nombre'), max_length=150)
    segundo_nombre = models.CharField(_lazy('segundo nombre'), max_length=150, blank=True)
    primer_apellido = models.CharField(_lazy('primer apellido'), max_length=150)
    segundo_apellido = models.CharField(_lazy('segundo apellido'), max_length=150, blank=True)
    genero = models.CharField(_lazy('género'), max_length=1, choices=GENEROS)
    fecha_nacimiento = models.DateField(_lazy('fecha de nacimiento'))
    fecha_ingreso = models.DateField(_lazy('fecha de ingreso'), blank=True, null=True)
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    numero_documento = models.CharField(_lazy('número de documento'), max_length=20, unique=True)
    estado_civil = models.CharField(_lazy('estado civil'), max_length=2, choices=ESTADOS_CIVILES, blank=True)
    zona = models.CharField(_lazy('zona'), max_length=1, choices=ZONAS, blank=True)
    direccion = models.CharField(_lazy('dirección'), max_length=200, blank=True)
    telefono = models.CharField(_lazy('telefono'), max_length=10, blank=True)
    celular = models.CharField(_lazy('celular'), max_length=15, blank=True)
    telefono2 = models.CharField(_lazy('telefono2'), max_length=100, blank=True)
    email = models.EmailField(_lazy('email'), blank=True)
    grupo_sanguineo = models.CharField(_lazy('grupo sanguineo'), max_length=3, choices=GRUPOS_SANGUINEOS, blank=True)
    grupo_etnico = models.CharField(_lazy('grupo etnico'), max_length=1, choices=GRUPOS_ETNICOS, blank=True)
    activo = models.BooleanField(_lazy('activo'), default=True)
    profesion = models.ForeignKey('globales.Profesion', related_name='pacientes', verbose_name=_lazy('profesión'), null=True, blank=True)
    lugar_nacimiento = models.ForeignKey('globales.Poblado', related_name='pacientes_nacidos_en', verbose_name=_lazy('nacio en'), null=True, blank=True)
    lugar_residencia = models.ForeignKey('globales.Poblado', related_name='pacientes_viven_en', verbose_name=_lazy('donde vive'), null=True, blank=True)
    foto = models.ImageField(upload_to=paciente_foto_path, verbose_name=_lazy('foto'), blank=True)
    firma = models.ImageField(upload_to=paciente_firma_path, verbose_name=_lazy('firma'), blank=True)
    procedencia = models.CharField(_lazy('como se entero'), max_length=2, choices=PROCEDENCIAS, blank=True)
    creado_el = models.DateField(auto_now_add=True)

    # Datos responsable
    parentesco_responsable = models.CharField(_lazy('parentesco del responsable'), max_length=3, choices=PARENTESCOS, blank=True)
    nombre_responsable = models.CharField(_lazy('nombre completo del responsable'), max_length=300, blank=True)
    direccion_responsable = models.CharField(_lazy('dirección del responsable'), max_length=200, blank=True)
    telefono_responsable = models.CharField(_lazy('telefono del responsable'), max_length=200, blank=True)

    # Menores de edad
    identificacion_padre = models.CharField(_lazy('identificación del padre'), max_length=15, blank=True)
    nombre_padre = models.CharField(_lazy('nombre completo del padre'), max_length=300, blank=True)
    telefono_padre = models.CharField(_lazy('telefono del padre'), max_length=200, blank=True)
    identificacion_madre = models.CharField(_lazy('identificación de la madre'), max_length=15, blank=True)
    nombre_madre = models.CharField(_lazy('nombre completo de la madre'), max_length=300, blank=True)
    telefono_madre = models.CharField(_lazy('telefono de la madre'), max_length=200, blank=True)

    # Datos de la empresa
    empresa = models.CharField(_lazy('empresa donde labora'), max_length=100, blank=True)
    direccion_empresa = models.CharField(_lazy('direccion empresa'), max_length=100, blank=True)
    telefono_empresa = models.CharField(_lazy('telefono empresa'), max_length=100, blank=True)

    objects = PacienteManager()

    class Meta:
        verbose_name = _lazy('paciente')
        verbose_name_plural = _lazy('pacientes')
        ordering = ['primer_nombre', 'primer_apellido']
        permissions = [
            ('can_add_paciente', 'Puede crear pacientes'),
            ('can_edit_paciente', 'Puede editar pacientes'),
            ('can_see_paciente', 'Puede ver los datos de un paciente'),
        ]

    def __str__(self):
        return '{} {} {} {}'.format(self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido)

    @property
    def edad(self):
        """:returns: Edad del paciente"""

        return self.edad_relativa(timezone.now().today())
    
    @property
    def is_menor_edad(self):
        """:returns: Booleano que indica si el paciente es menor de edad."""

        valor, unidad = self.edad.split(' ')
        return unidad == 'Dias' or unidad == 'Meses' or (unidad == 'Años' and int(valor) < 18)

    @property
    def ultimo_acompanante(self):
        """
        :returns:
            Retorna el ultimo acompañante con el que ha venido el paciente. Si el paciente no tiene ninguna orden
            registrada devuelve ``None``.
        """

        with suppress(models.ObjectDoesNotExist):
            ultima_orden = self.ordenes.latest('fecha_orden')
            return ultima_orden.acompanante

        return None
    
    @cached_property
    def tipo_usuario(self):
        """
        :returns:
            Retorna el tipo de usuario del paciente.
        """

        with suppress(models.ObjectDoesNotExist):
            return self.ordenes.latest('fecha_orden').tipo_usuario
        
        return None
    
    @property
    def tipo_usuario_display(self):
        """
        :returns:
            Retorna el nombre del tipo de usuario del paciente.
        """

        TIPOS_USUARIO = self.ordenes.model.TIPOS_USUARIO
        if self.tipo_usuario:
            return list(filter(lambda o: o[0] == self.tipo_usuario, TIPOS_USUARIO))[0][1]

        return None

    @cached_property
    def afiliacion(self):
        """
        :returns:
            Retorna la afiliacion del paciente.
        """

        with suppress(models.ObjectDoesNotExist):
            return self.ordenes.latest('fecha_orden').afiliacion
        
        return None

    @property
    def afiliacion_display(self):
        """
        :returns:
            Retorna el nombre de la afiliacion del paciente.
        """

        AFILIACIONES = self.ordenes.model.AFILIACIONES
        if self.afiliacion:
            return list(filter(lambda o: o[0] == self.afiliacion, AFILIACIONES))[0][1]
        
        return None

    @property
    def entidad(self):
        """
        :returns:
            Retorna la entidad del paciente.
        """

        with suppress(models.ObjectDoesNotExist):
            return self.ordenes.latest('fecha_orden').plan
        
        return None
    
    # Permissions
    def can_edit(self, user):
        return user.has_perm('pacientes.can_edit_paciente')

    def edit_url(self, user):
        """
        :returns:
            La url para editar el paciente si el usuario tiene permisos, sino, retorna ``None``.
        """

        warnings.warn('Deprecated method usar detail_url instead', DeprecationWarning)
        if self.can_edit(user):
            return reverse('pacientes:detalle', kwargs={'pk': self.pk})
        
        return None

    def detail_url(self, user):
        """
        :returns:
            La url para ver el detalle/editar paciente si el usuario tiene permisos, sino, retorna ``None``.
        """

        if user.has_perm('pacientes.can_see_paciente') or self.can_edit(user):
            return reverse('pacientes:detalle', kwargs={'pk': self.pk})
        
        return None
    
    def citas_url(self, user):
        """
        :returns:
            La url de las citas asociadas al paciente si el usuario no tiene permisos, sino, retorna ``None``.
        """

        # if user.has_perm('agenda.can_see_todas_citas'):
        #     return reverse('pacientes:citas', kwargs={'pk': self.pk})
        
        return None

    def tratamientos_url(self, user):
        """
        :returns:
            La url de los tratamientos asociados al paciente si el usuario no tiene permisos, sino, retorna ``None``.
        """

        if user.has_perm('pacientes.can_see_orden'):
            return reverse('pacientes:tratamientos', kwargs={'pk': self.pk})
        
        return None

    def pagos_url(self, user):
        """
        :returns:
            La url de los pagos de hechos por el paciente si el usuario no tiene permisos, sino, retorna ``None``.
        """

        if user.has_perm('facturacion.can_see_recibos_caja'):
            return reverse('pacientes:pagos', kwargs={'pk': self.pk})
        
        return None

    def edad_relativa(self, date):
        edad = date.year - self.fecha_nacimiento.year

        meses = abs(date.month - self.fecha_nacimiento.month)
        if edad == 0 and meses == 0:
            dias = abs(date.day - self.fecha_nacimiento.day)
            return '{} Dias'.format(dias)

        if edad == 0:
            return '{} Meses'.format(meses)

        return '{} Años'.format(edad)

    def historias_url(self, user):
        """
        :returns:
            La url de las historias del paciente si el usuario no tiene permisos, sino, retorna ``None``.
        """

        if user.has_perm('historias.puede_ver_historias'):
            return reverse('pacientes:historias', kwargs={'pk': self.pk})
        
        return None

    def get_historias(self):
        """
        :returns:
            Retorna un ``Queryset`` de las historias hechas por el paciente.
        """
        from historias.models import Historia
        return Historia.objects.filter(sesion__servicio__orden__paciente=self)

class Orden(UpdateModelMixin, models.Model):
    """Modelo que maneja la información de una orden de un paciente."""

    COTIZANTE = 'C'
    BENEFICIARIO = 'B'
    SUBSIDIADO = 'A'
    PARTICULAR = 'P'
    VINCULADO = 'V'
    OTRO = 'O'
    AFILIACIONES = (
        (COTIZANTE, _lazy('Cotizante')),
        (BENEFICIARIO, _lazy('Beneficiario')),
        (SUBSIDIADO, _lazy('Subsidiado')),
        (PARTICULAR, _lazy('Particular')),
        (VINCULADO, _lazy('Vinculado')),
        (OTRO, _lazy('Otro'))
    )

    CONTRIBUTIVO = 'C'
    TIPOS_USUARIO = (
        (CONTRIBUTIVO, _lazy('Contributivo')),
        (SUBSIDIADO, _lazy('Subsidiado')),
        (VINCULADO, _lazy('Vinculado')),
        (PARTICULAR, _lazy('Particular')),
        (OTRO, _lazy('Otro'))
    )

    paciente = models.ForeignKey(Paciente, related_name='ordenes', verbose_name=_lazy('paciente'))
    plan = models.ForeignKey('servicios.Plan', related_name='ordenes', verbose_name=_lazy('cliente'))
    fecha_orden = models.DateField(_lazy('Fecha de la orden'), auto_now_add=True)
    afiliacion = models.CharField(_lazy('afiliación'), max_length=1, choices=AFILIACIONES, default=PARTICULAR, blank=True)
    tipo_usuario = models.CharField(_lazy('tipo de usuario'), max_length=1, choices=TIPOS_USUARIO, default=PARTICULAR, blank=True)
    asistio_acompanante = models.BooleanField(_lazy('asistio con acompañante'), default=False)
    medico_ordena = models.CharField(_lazy('medico que ordena'), max_length=150, blank=True)
    institucion = models.ForeignKey(
        'organizacional.Institucion', related_name='ordenes',
        verbose_name=_lazy('entidad que prestará el servicio')
    )
    servicios = models.ManyToManyField(
        'servicios.Servicio', through='ServicioRealizar', related_name='ordenes', verbose_name=_lazy('servicios')
    )

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'
        permissions = [
            ('can_see_orden', 'Puede ver la orden'),
            ('can_edit_orden', 'Puede editar la orden despues de que ya se haya iniciado el tratamiento'),
            ('puede_ver_orden_sin_paciente', 'Puede ver la orden sin que el paciente haya llegado a la cita'),
        ]

    def __str__(self):
        return '{0} - {1}'.format(str(self.paciente), self.pk)

    def get_absolute_url(self):
        return reverse('pacientes:ordenes-detalle', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        if not self.asistio_acompanante and hasattr(self, 'acompanante'):
            self.acompanante.delete()
        super().save(*args, **kwargs)
    
    def _save_acompanante(self, **kwargs):
        """Guarda los datos del acompanante."""

        if hasattr(self, 'acompanante'):
            self.acompanante.update(**kwargs)
        else:
            Acompanante.objects.create(orden=self, **kwargs)
    
    @transaction.atomic
    def update(self, **kwargs):
        """Actualiza los datos de la orden."""

        acompanante_data = kwargs.pop('acompanante', None)
        update_rates = kwargs.get('plan') != self.plan or kwargs.get('institucion') != self.institucion
        for field, value in kwargs.items():
            setattr(self, field, value)
        
        if self.asistio_acompanante:
            self._save_acompanante(**acompanante_data)
        
        if update_rates:
            for tratamiento in self.servicios_realizar.all():
                valor = getattr(self.plan.tarifa(tratamiento.servicio, self.institucion), 'valor', 0)
                tratamiento.valor = valor
                tratamiento.save()
        self.save()

    def total_pagado(self):
        """Valor pagado por el paciente."""

        return sum(map(lambda o: o.total_pagado, self.servicios_realizar.all()))

    # Permisos
    def can_edit(self, user):
        """Indica si se puede editar la orden."""

        if user.has_perm('pacientes.can_edit_orden'):
            return True

        NO_INI = self.servicios_realizar.model.NO_INICIADO
        return all([estado == NO_INI for estado in self.servicios_realizar.values_list('estado', flat=True)])

class ServicioRealizar(UpdateModelMixin, models.Model):
    """Modelo que guarda los servicios que maneja una orden."""

    INICIADO = 'IN'
    CANCELADO = 'CA'
    TERMINADO = 'TE'
    NO_INICIADO = 'NI'
    ESTADOS = (
        (NO_INICIADO, _lazy('No iniciado')),
        (INICIADO, _lazy('Iniciado')),
        (TERMINADO, _lazy('Terminado')),
        (CANCELADO, _lazy('Cancelado')),
    )

    cantidad = models.PositiveIntegerField(_lazy('cantidad'), default=1)
    estado = models.CharField(max_length=2, choices=ESTADOS, default=NO_INICIADO)
    orden = models.ForeignKey(Orden, related_name='servicios_realizar', verbose_name=_lazy('orden'))
    is_una_cita = models.BooleanField(default=False, help_text='Indica si el tratamiento se hace en una sola cita')
    servicio = models.ForeignKey('servicios.Servicio', related_name='servicios_realizar', verbose_name=_lazy('servicio'))
    valor = models.DecimalField(_lazy('valor'), max_digits=25, decimal_places=15, default=0, help_text='Valor por sesión')
    is_coopago_total = models.BooleanField(default=False, help_text='Indica si el valor del coopago es por todas las sesiones')
    coopago = models.DecimalField(_lazy('coopago/moderadora'), max_digits=25, decimal_places=15, default=0, help_text='Coopago por sesión o total según is_coopago_total')
    num_sesiones_coopago = models.PositiveIntegerField(_lazy('numero de sesiones por coopago'), blank=True, null=True)
    
    # Auditorias
    recibido_por = models.ForeignKey('organizacional.Empleado', related_name='servicios_recibidos', blank=True, null=True)
    recibido_at = models.DateField(null=True, blank=True)
    verificado_por = models.ForeignKey('organizacional.Empleado', related_name='servicios_verificados', blank=True, null=True)
    verificado_at = models.DateField(null=True, blank=True)
    verificado_inicio_por = models.ForeignKey('organizacional.Empleado', related_name='servicios_verificados_inicio', blank=True, null=True)
    verificado_inicio_at = models.DateField(null=True, blank=True)
    verificado_inicio_admin_por = models.ForeignKey('organizacional.Empleado', related_name='tratamientos_verificados_inicio_admin', blank=True, null=True)
    verificado_inicio_admin_at = models.DateField(null=True, blank=True)

    objects = ServicioRealizarManager()

    class Meta:
        ordering = ['id']
        verbose_name = 'tratamiento'
        verbose_name_plural = 'tratamientos'
        permissions = [
            ('can_verificar_orden_inicio_tratamiento', 'Verificar los datos de la orden al inicio del tratamiento'),
            ('can_recibir_pacientes_terminaron_tratamiento', 'Puede recibir los pacientes que terminaron tratamiento'),
            ('can_verificar_pacientes_terminaron_tratamiento', 'Puede verificar los pacientes que terminaron tratamiento'),
        ]

    def __str__(self):
        return '{} - {} - {}'.format(self.orden_id, self.pk, self.servicio.nombre)

    @property
    def paciente(self):
        return self.orden.paciente

    @property
    def convenio(self):
        return self.orden.plan

    @property
    def entidad(self):
        return self.orden.plan.cliente

    @property
    def coopago_total(self):
        """Valor total del coopago."""

        if self.is_coopago_total:
            return self.coopago
        
        if self.num_sesiones_coopago:
            return math.ceil(self.cantidad / self.num_sesiones_coopago) * self.coopago

        return self.coopago * self.cantidad

    @property
    def coopago_bruto(self):
        """Valor del coopago sin IVA."""

        return self.coopago - self.iva_coopago

    @property
    def iva_coopago(self):
        """Valor del IVA del coopago."""

        if self.coopago == 0:
            return 0

        convenio = self.orden.plan
        if convenio.cliente.discriminar_iva:
            _tarifas = self.servicio.tarifas.all()
            tarifas = list(filter(
                lambda t: t.plan_id == convenio.id and t.institucion_id == self.orden.institucion_id,
                _tarifas
            ))
            if tarifas:
                return tarifas[0].iva_coopago

        return 0

    @property
    def valor_total(self):
        """Retorna el valor total de la sesión."""

        return self.cantidad * self.valor

    @property
    def valor_pagar(self):
        """"Valor neto a pagar(Cliente)."""

        return self.valor - self.coopago

    @property
    def total_pagado(self):
        """Valor pagado por el paciente."""

        _total_pagado = getattr(self, '_total_pagado', -1)
        if _total_pagado == -1:
            _total_pagado =  self.recibos_caja.no_anulados().aggregate(total=models.Sum('valor'))['total']

        return _total_pagado or 0

    @property
    def saldo_paciente(self):
        """Saldo que le queda por pagar al paciente."""

        return self.coopago_total - self.total_pagado

    @property
    def saldo_sesiones(self):
        """
        Saldo de las sesiones atendidas. Según el valor se indica si el paciente tiene deuda, al día o tiene saldo a favor.

        - Deuda: Si el valor es negativo.
        - Al día: Si el valor es 0.
        - Saldo a favor: Si el valor es positivo.
        """

        num_atendidas = self.numero_sesiones_atendidas()

        valor_actual = num_atendidas * self.coopago
        if self.is_coopago_total and num_atendidas > 0:
            valor_actual = self.coopago
        elif self.num_sesiones_coopago is not None and num_atendidas > 0:
            valor_actual = math.ceil(num_atendidas / self.num_sesiones_coopago) * self.coopago

        return self.total_pagado - valor_actual

    @property
    def numero_sesiones_faltantes(self):
        """Retorna el numero de sesiones no han sido atendidas."""

        num_atendidas = self.numero_sesiones_atendidas()
        if self.is_una_cita and num_atendidas == 1:
            return 0

        return self.cantidad - num_atendidas
    
    @property
    def inicio_tratamiento(self):
        """Fecha de inicio del tratamiento."""

        _fecha_inicio = getattr(self, '_fecha_inicio', None)
        return _fecha_inicio or self.citas.all().datetimes('inicio', 'minute').first()
    
    @property
    def fin_tratamiento(self):
        """Fecha de fin del tratamiento."""

        fecha = None
        if self.estado in [self.TERMINADO, self.CANCELADO]:
            fecha = self.citas.atendidas().datetimes('inicio', 'minute').last()
            if not fecha:
                fecha = self.citas.canceladas().datetimes('inicio', 'minute').first()
        
        return fecha or self.citas.all().datetimes('inicio', 'minute').last()
    
    @property
    def medicos(self):
        """Retorna los profesionales de la salud que atendieron el servicio."""

        Empleado = import_string('organizacional.models.Empleado')
        return Empleado.objects.filter(id__in=self.citas.values('medico'))

    def valor_pagar_medico(self, medico):
        """Retorna el valor a pagar a un medico."""

        if isinstance(medico, str):
            Empleado = import_string('organizacional.models.Empleado')
            medico = Empleado.objects.get(id=medico)

        return self.valor * (Decimal(medico.porcentaje_pago) / 100)

    def numero_sesiones_atendidas(self, medico=None, desde=None, hasta=None):
        """Retorna el número de sesiones atendidas."""

        _num_citas = getattr(self, '_num_citas_atendidas', -1)
        if _num_citas == -1:
            citas = self.citas.atendidas().fecha_entre(desde, hasta)
            if medico:
                citas = citas.by_medico(medico)

            _num_citas = citas.count()

        _num_citas = _num_citas or 0
        return self.cantidad if _num_citas > 0 and self.is_una_cita else _num_citas

    # Permisos
    def can_reagendar_citas(self):
        """Solo se pueden reagendar citas si la cantidad de citas del tratamiento es mayor al número de citas
        que no estan excusadas, no asistio y no atendidas.
        """

        if self.estado == self.CANCELADO:
            return False

        HistorialEstado = import_string(HISTORIAL_ESTADO_PATH)
        numero_validas = self.citas.exclude_by_estados([
            HistorialEstado.EXCUSADA,
            HistorialEstado.NO_ASISTIO,
            HistorialEstado.NO_ATENDIDA
        ]).count()
        cantidad = 1 if self.is_una_cita else self.cantidad
        return numero_validas < cantidad

    def can_verificar_inicio_tratamiento(self, user):
        """Indica si puede verificar el inicio del tratamiento."""

        if user.has_perm('pacientes.can_verificar_orden_inicio_tratamiento'):
            return True

        return False

    def can_edit(self, user):
        """Indica si se puede editar el tratamiento."""

        if user.has_perm('pacientes.can_edit_orden'):
            return True

        return self.estado == self.NO_INICIADO
    
    def can_edit_valor(self, user):
        """Indica si puede editar el valor por sesión."""

        return user.has_perm('pacientes.can_edit_orden')

    # URLs
    def control_citas_url(self):
        """URL del control de citas."""

        return reverse('pacientes:control-citas', kwargs={'pk': self.id})

    def orden_url(self, user):

        if user.has_perm('pacientes.puede_ver_orden_sin_paciente') or user.has_perm('pacientes.puede_ver_orden'):
            return reverse('pacientes:ordenes-detalle', kwargs={'pk': self.orden_id})
        
        return None

    def _actualizar_servicio(self, servicio):
        """Actualiza el servicio y su valor en la entidad no persiste el cambio en la bd."""

        orden = self.orden
        self.servicio = servicio
        tarifa = orden.plan.tarifa(servicio, orden.institucion)
        self.valor = getattr(tarifa, 'valor', 0)
        self.coopago = getattr(tarifa, 'coopago', 0)
    
    def _eliminar_citas(self, total, a_eliminar):
        """Elimina el numero de citas escogidas."""

        self.citas.filter(id__in=self.citas.all()[total - a_eliminar:]).delete()

    def _actualizar_cantidad(self, cantidad, empleado, is_una_cita):
        """Actualiza la cantidad de sesiones del servicio a realizar."""

        if self.cantidad != cantidad or self.is_una_cita != is_una_cita:
            cantidad_actual = self.citas.count()
            cantidad_citas = 1 if is_una_cita else cantidad
            if cantidad_actual != cantidad_citas:
                if cantidad_citas > cantidad_actual:
                    self._agendar_futuras_citas(cantidad_citas - cantidad_actual, empleado)
                else:
                    self._eliminar_citas(cantidad_actual, cantidad_actual - cantidad_citas)
            self.is_una_cita = is_una_cita
            self.cantidad = cantidad
            self.cambiar_estado()

    @transaction.atomic
    def update(self, servicio, cantidad, coopago, empleado, num_sesiones_coopago=None, is_coopago_total=False, valor=None, is_una_cita=False):
        """Actualiza los datos del servicio prestado."""

        self._actualizar_servicio(servicio)
        self._actualizar_cantidad(cantidad, empleado, is_una_cita)
        self.num_sesiones_coopago = num_sesiones_coopago
        self.is_coopago_total = is_coopago_total
        self.coopago = coopago
        if valor:
            self.valor = valor

        self.save()

    def cancelar(self):
        """Cancela el servicio prestado."""

        self.estado = self.CANCELADO
        self.save()
    
    def cambiar_estado(self):
        """Cambia el estado del tratamiento."""

        cantidad = 1 if self.is_una_cita else self.cantidad
        if self.citas.atendidas().count() == cantidad:
            self.estado = self.TERMINADO
            self.save()
        elif self.estado != self.INICIADO and self.citas.atendidas().exists():
            self.estado = self.INICIADO
            self.save()
        elif self.estado != self.CANCELADO and self.citas.canceladas().exists():
            self.cancelar()
    
    @transaction.atomic
    def reagendar_citas(self, empleado, cantidad=None):
        """Reagenda las citas que se encuentran excusadas, no atendidas y no asistio."""

        HistorialEstado = import_string(HISTORIAL_ESTADO_PATH)

        num_reagendar = cantidad
        if not cantidad:
            numero_validas = self.citas.exclude_by_estados([
                HistorialEstado.EXCUSADA,
                HistorialEstado.NO_ASISTIO,
                HistorialEstado.NO_ATENDIDA
            ]).count()
            num_reagendar = self.cantidad - numero_validas

        self._agendar_futuras_citas(num_reagendar, empleado)
    
    def _agendar_futuras_citas(self, cantidad, empleado):
        """Agenda la cantidad de citas futuras.

        :param cantidad: Es la cantidad de citas que se van a crear
        """

        ultima_cita = self.citas.last()
        fecha = ultima_cita.inicio + datetime.timedelta(days=1)

        agendar_multiples_citas = import_string('agenda.services.agendar_multiples_citas')
        agendar_multiples_citas(
            cantidad=cantidad,
            empleado=empleado,
            desde=fecha.date(),
            tratamiento=self,
            medico=ultima_cita.medico,
            aut=ultima_cita.autorizacion,
            sucursal=ultima_cita.sucursal,
            duracion=ultima_cita.duracion,
            hora=timezone.localtime(fecha).timetz(),
            fecha_aut=ultima_cita.fecha_autorizacion,
        )

Tratamiento = ServicioRealizar

class Acompanante(UpdateModelMixin, models.Model):
    """Modelo que guarda la información del acompañante de un paciente según el ordenamiento."""

    TIO = 'T'
    OTRO = 'O'
    HIJO = 'I'
    PADRE = 'P'
    MADRE = 'M'
    AMIGO = 'AM'
    ABUELO = 'A'
    PRIMO = 'PR'
    HERMANO = 'H'
    CONYUGUE = 'C'
    PARENTESCOS = (
        (PADRE, _lazy('Padre')),
        (MADRE, _lazy('Madre')),
        (HERMANO, _lazy('Hermano')),
        (HIJO, _lazy('Hijo')),
        (ABUELO, _lazy('Abuelo')),
        (TIO, _lazy('Tio')),
        (PRIMO, _lazy('Primo')),
        (CONYUGUE, _lazy('Conyugue')),
        (AMIGO, _lazy('Amigo')),
        (OTRO, _lazy('Otro'))
    )

    orden = models.OneToOneField(Orden, verbose_name=_lazy('orden'))
    parentesco = models.CharField(_lazy('parentesco'), max_length=3, choices=PARENTESCOS)
    nombre = models.CharField(_lazy('nombre completo'), max_length=200)
    direccion = models.CharField(_lazy('dirección'), max_length=200)
    telefono = models.CharField(_lazy('teléfono'), max_length=200)

    class Meta:
        verbose_name = _lazy('acompañate')
        verbose_name_plural = _lazy('acompañates')

    def __str__(self):
        return self.nombre
    
    @transaction.atomic
    def update(self, **kwargs):
        """Actualiza los datos del acompanante."""

        for field, value in kwargs.items():
            setattr(self, field, value)  
