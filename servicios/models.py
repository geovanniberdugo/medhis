from django.db import models
from django.utils.translation import ugettext_lazy as _lazy
from .managers import ServicioManager, TipoManager

class Tipo(models.Model):
    """Modelo para guardar los tipos de servicio que presta un clinete."""

    OTRO = '00'
    CONSULTA = '01'
    ESTANCIA = '06'
    HONORARIO = '07'
    DERECHO_SALA = '08'
    BANCO_SANGRE = '10'
    PROTESIS_ORTESIS = '11'
    MEDICAMENTOS_POS = '12'
    TRASLADO_PACIENTE = '14'
    MEDICAMENTOS_NO_POS = '13'
    MATERIALES_INSUMOS = '09'
    PROCEDIMIENTO_DIAGNOSTICO = '02'
    PROCEDIMIENTO_PROMOCION_PREVENCION = '05'
    PROCEDIMIENTO_TERAPEUTICO_QUIRURGICO = '04'
    PROCEDIMIENTO_TERAPEUTICO_NO_QUIRURGICO = '03'
    CLASES = (
        (OTRO, _lazy('Otro')),
        (CONSULTA, _lazy('Consulta')),
        (ESTANCIA, _lazy('Estancia')),
        (HONORARIO, _lazy('Honorario')),
        (DERECHO_SALA, _lazy('Derecho de sala')),
        (BANCO_SANGRE, _lazy('Banco de sangre')),
        (MEDICAMENTOS_POS, _lazy('Medicamento POS')),
        (PROTESIS_ORTESIS, _lazy('Prótesis y órtesis')),
        (TRASLADO_PACIENTE, _lazy('Traslado de paciente')),
        (MEDICAMENTOS_NO_POS, _lazy('Medicamento no POS')),
        (MATERIALES_INSUMOS, _lazy('Materiales e insumos')),
        (PROCEDIMIENTO_DIAGNOSTICO, _lazy('Procedimiento de diagnóstico')),
        (PROCEDIMIENTO_TERAPEUTICO_QUIRURGICO, _lazy('Procedimiento terapéutico quirúrgico')),
        (PROCEDIMIENTO_PROMOCION_PREVENCION, _lazy('Procedimiento de promoción y prevención')),
        (PROCEDIMIENTO_TERAPEUTICO_NO_QUIRURGICO, _lazy('Procedimiento terapéutico no quirúrgico')),
    )

    in_indicadores = models.BooleanField(default=True)
    nombre = models.CharField(_lazy('nombre'), max_length=100)
    clase = models.CharField(_lazy('clase'), max_length=3, choices=CLASES)

    objects = TipoManager()

    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'tipos'
    
    def __str__(self):
        return self.nombre
    
    @property
    def is_consulta(self):
        """Indica si el tipo es de clase consulta."""

        return self.clase == self.CONSULTA
    
    @property
    def is_procedimiento(self):
        """Indica si el tipo es de clase procedimiento."""

        return self.clase in [
            self.PROTESIS_ORTESIS,
            self.PROCEDIMIENTO_DIAGNOSTICO,
            self.PROCEDIMIENTO_TERAPEUTICO_QUIRURGICO,
            self.PROCEDIMIENTO_TERAPEUTICO_NO_QUIRURGICO
        ]

class Servicio(models.Model):
    """Modelo para guardar la información de los servicios que ofrece un cliente."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    codigo = models.CharField(_lazy('código'), max_length=100, blank=True)
    abreviatura = models.CharField(_lazy('abreviatura'), max_length=100)
    cups = models.CharField(_lazy('cups'), max_length=100, blank=True)
    costo = models.PositiveIntegerField(_lazy('costo'), blank=True, null=True, default=0)
    tipo = models.ForeignKey(Tipo, related_name='servicios', verbose_name=_lazy('tipo'))

    objects = ServicioManager()

    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

    @property
    def clase(self):
        """Indica a la clase o naturaleza del servicio."""

        return self.tipo.clase
    
    @property
    def tipo_rips(self):
        """Indica el tipo de rips que genera el servicio."""

        if self.tipo.is_consulta:
            return 'consulta'
        elif self.tipo.is_procedimiento:
            return 'procedimiento'
        
        return None

class Cliente(models.Model):
    """Representa la información de los clientes a los cuales un tenant(IPS) le presta sus servicio."""

    MP = 'MP'
    EPS = 'EPS'
    ARL = 'ARL'
    OTRO = 'OTRO'
    TIPOS = (
        (EPS, 'EPS'),
        (ARL, 'ARL'),
        (MP, 'Prepagada'),
        (OTRO, 'Otras entidades'),
    )

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    razon_social = models.CharField(_lazy('razón social'), max_length=200)
    nit = models.CharField(_lazy('nit'), max_length=50)
    direccion = models.CharField(_lazy('dirección'), max_length=100, blank=True)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)
    codigo = models.CharField(_lazy('código'), max_length=100, blank=True)
    tipo = models.CharField(max_length=5, choices=TIPOS)
    ciudad = models.ForeignKey(
        'globales.Poblado', related_name='clientes', verbose_name=_lazy('ciudad'), blank=True, null=True
    )
    sesiones_autorizacion = models.IntegerField(
        _lazy('sesiones por autorización'), null=True, blank=True,
        help_text=_lazy('Indica el # de sesiones que le aplica la misma autorización. Si esta vació se usa la misma autorización para todas las sesiones.')
    )

    # Datos de facturación
    discriminar_iva = models.BooleanField(_lazy('Discriminar IVA'), default=False)
    factura_paciente = models.BooleanField(_lazy('Factura a nombre de paciente'), default=False)
    puc_facturacion = models.CharField(_lazy('cuenta puc facturacion'), max_length=100, blank=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
    
    def __str__(self):
        return self.nombre

    @property
    def tipo_display(self):
        """Devuelve el nombre del tipo."""

        return list(filter(lambda o: o[0] == self.tipo, self.TIPOS))[0][1]

class Plan(models.Model):
    """Modelo para guardar información de los planes que manejan los clientes."""

    nombre = models.CharField(_lazy('plan'), max_length=200)
    cliente = models.ForeignKey(Cliente, related_name='planes', verbose_name=_lazy('cliente'))
    servicios = models.ManyToManyField(Servicio, through='tarifa', related_name='planes', verbose_name=_lazy('servicios'))

    class Meta:
        verbose_name = 'plan'
        verbose_name_plural = 'planes'
    
    def __str__(self):
        return '{} - {}'.format(self.cliente.nombre, self.nombre)
    
    @property
    def sesiones_autorizacion(self):
        """Indica el número de sesiones que tienen la misma autorización."""

        return self.cliente.sesiones_autorizacion
    
    @property
    def requiere_autorizacion(self):
        """Indica si requiere autorización."""

        return not self.sesiones_autorizacion == 0
    
    def tarifa(self, servicio, institucion):
        """Retorna la tarifa de un servicio especifco."""

        return self.tarifas.filter(servicio=servicio, institucion=institucion).first()

class Tarifa(models.Model):
    """Modelo para guardar las tarifas de los servicio por cada plan de los clientes."""

    plan = models.ForeignKey(Plan, related_name='tarifas', verbose_name=_lazy('convenio'))
    institucion = models.ForeignKey('organizacional.Institucion', related_name='tarifas')
    servicio = models.ForeignKey(Servicio, related_name='tarifas', verbose_name=_lazy('servicio'))
    valor = models.DecimalField(_lazy('valor'), max_digits=25, decimal_places=15, help_text='Valor que se cobra al cliente')
    coopago = models.DecimalField(_lazy('coopago'), max_digits=25, decimal_places=15, help_text='Valor del coopago con IVA')
    iva_coopago = models.DecimalField(_lazy('iva coopago'), max_digits=25, decimal_places=15, default=0)

    class Meta:
        verbose_name = 'tarifa'
        verbose_name_plural = 'tarifas'
        unique_together = ('servicio', 'plan', 'institucion')
        permissions = [
            ('can_add_tarifa', 'Puede agregar tarifas'),
        ]

    def __str__(self):
        return '{}-{}: ${}'.format(self.plan.nombre, self.servicio.nombre, self.valor)
