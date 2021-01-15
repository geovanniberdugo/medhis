from datetime import date
from contextlib import suppress
from django.urls import reverse
from django.utils import timezone
from django.db import models, transaction
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _lazy
from .managers import FacturaManager, DetalleFacturaManager, ReciboCajaManager, CajaManager, ParametroFacturaSiigoManager


class ParametroFacturaSiigo(models.Model):
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

    tipo_servicio = models.ForeignKey('servicios.Tipo', related_name='parametros_facturacion_siigo')
    tipo_cliente = models.CharField(max_length=5, choices=TIPOS)
    cuenta_puc = models.CharField(max_length=100)
    codigo_linea = models.CharField(max_length=5, blank=True)
    codigo_producto = models.CharField(max_length=5, blank=True)

    objects = ParametroFacturaSiigoManager()

    class Meta:
        unique_together = ('tipo_cliente', 'tipo_servicio')
    
    def __str__(self):
        return '{} {}'.format(self.tipo_servicio, self.get_tipo_cliente_display())

class ReciboCaja(models.Model):
    """Modelo que maneja la información de los pagos de los pacientes."""

    EFECTIVO = 'E'
    TARJETA = 'T'
    CONSIGNACION = 'C'
    FORMAS_PAGO = (
        (EFECTIVO, _lazy('Efectivo')),
        (TARJETA, _lazy('Tarjeta')),
        (CONSIGNACION, _lazy('Consignación/Transferencia')),
    )

    numero = models.IntegerField(_lazy('número'))
    servicio_prestado = models.ForeignKey('pacientes.ServicioRealizar', related_name='recibos_caja', verbose_name=_lazy('servicio'))
    forma_pago = models.CharField(_lazy('forma de pago'), max_length=2, choices=FORMAS_PAGO)
    valor = models.DecimalField(_lazy('valor'), max_digits=25, decimal_places=15)
    fecha = models.DateField(_lazy('fecha'), auto_now_add=True)
    detalle = models.TextField(_lazy('detalle'), blank=True)
    empleado = models.ForeignKey('organizacional.Empleado', related_name='recibos_caja')
    sucursal = models.ForeignKey('organizacional.Sucursal', related_name='recibos_caja')

    # Datos anulacion
    razon_anulacion = models.TextField(blank=True)
    anulado_el = models.DateField(blank=True, null=True)
    anulado_por = models.ForeignKey('organizacional.Empleado', related_name='recibos_caja_anulados', blank=True, null=True)

    objects = ReciboCajaManager()
    
    class Meta:
        verbose_name = 'recibo de caja'
        verbose_name_plural = 'recibos de caja'
        permissions = [
            ('print_recibo', 'Puede imprimir recibos de caja'),
            ('can_see_recibos_caja', 'Puede ver los pagos de un paciente'),
            ('can_anular_recibos_caja', 'Puede anular pagos de pacientes'),
            ('can_contabilizar_recibo_caja', 'Puede contabilizar recibos de caja'),
        ]
    
    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.servicio_prestado_id, self.valor)
    
    @classmethod
    def nombre_consecutivo(self):
        """Retorna el nombre del consecutivo para los recibos de caja."""

        return 'recibo_caja'
    
    @property
    def get_absolute_url(self):
        return reverse('facturacion:recibo', kwargs={'pk': self.id})
    
    @property
    def paciente(self):
        """Retorna el paciente."""

        return self.servicio_prestado.orden.paciente
    
    @property
    def cliente(self):
        """Retorna el cliente."""

        return self.servicio_prestado.orden.plan.cliente
    
    @property
    def servicio(self):
        """Retorna el servicio que se pago"""

        return self.servicio_prestado.servicio

    # permiso
    def can_anular(self, user):
        return user.has_perm('facturacion.can_anular_recibos_caja')
    
    def anular(self, razon_anulacion, empleado):
        self.anulado_por = empleado
        self.razon_anulacion = razon_anulacion
        self.anulado_el = date.today()
        self.save()

class Caja(models.Model):
    
    empleado = models.ForeignKey('organizacional.Empleado', related_name='cajas')
    sucursal = models.ForeignKey('organizacional.Sucursal', related_name='cajas')
    pagos = models.DecimalField(_lazy('pagos'), max_digits=25, decimal_places=15, default=0)
    fecha = models.DateField(default=date.today)

    # Auditorias
    recibido_por = models.ForeignKey('organizacional.Empleado', related_name='cajas_recibidas', blank=True, null=True)
    recibido_at = models.DateField(null=True, blank=True)

    # Auditoria contabilidad
    verificado_por = models.ForeignKey('organizacional.Empleado', related_name='cajas_verificadas', blank=True, null=True)
    verificacion_correcta = models.BooleanField(help_text='Indica si los valores son correctos', default=True)
    observaciones_verificacion = models.TextField(blank=True)
    verificado_at = models.DateField(null=True, blank=True)

    objects = CajaManager()

    class Meta:
        verbose_name = 'caja'
        verbose_name_plural = 'cajas'
        ordering = ['-fecha', 'id']
        permissions = [
            ('can_edit_caja', 'Puede editar caja'),
            ('can_cerrar_caja', 'Puede cerrar caja'),
            ('can_see_todas_cajas', 'Puede ver todas las cajas'),
            ('can_recibir_caja', 'Puede recibir el dinero del cierre de caja'),
            ('can_see_transacciones_caja', 'Puede ver transacciones asociadas a una caja'),
        ]

    def __str__(self):
        return '{} - {}'.format(self.sucursal_id, self.fecha)
    
    def get_absolute_url(self):
        return reverse('facturacion:detalle-caja', kwargs={'pk': self.id})
    
    @property
    def total_recibido(self):
        """Retorna el dinero total que ingreso a la caja."""

        return self.detalles.aggregate(total=models.Sum('valor'))['total'] or 0

    @property
    def total(self):
        """Retorna el total de la caja (recibido - gastado)."""

        return self.total_recibido + self.pagos

    # Permissions
    def can_edit(self, user):
        """Indica si se puede editar."""

        return user.has_perm('facturacion.can_edit_caja')
    
    @transaction.atomic
    def verificar(self, empleado, **kwargs):
        """Verificacion de contabilidad de una caja"""

        for field, value in kwargs.items():
            setattr(self, field, value)

        self.verificado_por = empleado
        self.verificado_at = timezone.now()
        self.save()
        return self
    
    @transaction.atomic
    def update(self, detalles, **kwargs):
        """Actualiza la caja."""

        for field, value in kwargs.items():
            setattr(self, field, value)
        
        self.save()
        
        self.detalles.all().delete()
        DetalleCaja = self.detalles.model
        list(map(lambda o: DetalleCaja.objects.create(caja=self, **o), detalles))

class DetalleCaja(models.Model):

    EFECTIVO = 'E'
    TARJETA = 'T'
    CONSIGNACION = 'C'
    FORMAS_PAGO = (
        (EFECTIVO, _lazy('Efectivo')),
        (TARJETA, _lazy('Tarjeta')),
        (CONSIGNACION, _lazy('Consignación/Transferencia')),
    )

    caja = models.ForeignKey(Caja, related_name='detalles')
    forma_pago = models.CharField(_lazy('forma de pago'), max_length=2, choices=FORMAS_PAGO)
    valor = models.DecimalField(_lazy('valor'), max_digits=25, decimal_places=15)

    def __str__(self):
        return '{} - {} - {}'.format(self.caja_id, self.forma_pago, self.valor)

class Factura(models.Model):
    """Modelo que maneja la información de una factura."""

    numero = models.IntegerField(_lazy('número'))
    fecha_fin = models.DateField(_lazy('fecha fin'), blank=True, null=True)
    fecha_inicio = models.DateField(_lazy('fecha inicio'), blank=True, null=True)
    cliente = models.ForeignKey('servicios.Cliente', related_name='facturas')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='facturas', blank=True, null=True)
    institucion = models.ForeignKey('organizacional.Institucion', related_name='facturas')
    fecha_expedicion = models.DateTimeField(_lazy('fecha de expedicion'), default=timezone.now)
    observaciones = models.TextField(_lazy('observaciones'), blank=True)

    # Datos anulacion
    razon_anulacion = models.TextField(blank=True)
    anulado_el = models.DateField(blank=True, null=True)
    anulado_por = models.ForeignKey('organizacional.Empleado', related_name='facturas_anuladas', blank=True, null=True)

    objects = FacturaManager()

    class Meta:
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'
        unique_together = ('numero', 'institucion')
        permissions = [
            ('can_facturar', 'Puede facturar'),
            ('can_anular_facturas', 'Puede anular facturas'),
            ('can_eliminar_facturas', 'Puede eliminar facturas'),
        ]
    
    def __str__(self):
        return '{}'.format(self.numero)
    
    def get_absolute_url(self):
        return reverse('facturacion:detalle', kwargs={'pk': self.id})
    
    def subtotal(self):
        """Retorna la suma de los subtotales del detalle de la factura."""

        return (
            self.detalle
                .annotate(_sub=models.ExpressionWrapper(models.F('cantidad') * models.F('valor'), output_field=models.DecimalField()))
                .aggregate(_subtotal=models.Sum('_sub'))['_subtotal']
        )
    
    def total_coopago(self):
        """Retorna el total del coopago."""

        return self.detalle.aggregate(models.Sum('coopago'))['coopago__sum']

    def total_coopago_bruto(self):
        """Retorna el total del coopago bruto."""

        return self.detalle.aggregate(models.Sum('coopago_bruto'))['coopago_bruto__sum']
    
    def total_iva_coopago(self):
        """Retorna el total del iva del coopago."""

        return self.detalle.aggregate(models.Sum('iva_coopago'))['iva_coopago__sum']
    
    def total(self):
        """Retorna el total de la factura."""

        return sum(map(lambda o: o.subtotal(), self.detalle.all()))

    def cuenta_siigo(self):
        tipo_servicio = self.detalle.all()[0].servicio.tipo
        return tipo_servicio.parametros_facturacion_siigo.filter(tipo_cliente=self.cliente.tipo).first()

    def puc_subtotal(self):
        param = self.cuenta_siigo()
        return getattr(param, 'cuenta_puc', '')
    
    def codigo_linea(self):
        param = self.cuenta_siigo()
        return getattr(param, 'codigo_linea', '')
    
    def codigo_producto(self):
        param = self.cuenta_siigo()
        return getattr(param, 'codigo_producto', '')

    # permiso
    def can_anular(self, user):
        return user.has_perm('facturacion.can_anular_facturas')

    def can_eliminar(self, user):
        return user.has_perm('facturacion.can_eliminar_facturas')

class DetalleFactura(models.Model):
    """Modelo que guarda la información del detalle de una factura."""

    cantidad = models.IntegerField()
    factura = models.ForeignKey(Factura, related_name='detalle')
    valor = models.DecimalField(_lazy('valor'), max_digits=25, decimal_places=15, help_text='Valor unitario')
    coopago = models.DecimalField(_lazy('coopago'), max_digits=25, decimal_places=15, help_text='Coopago total')
    iva_coopago = models.DecimalField(_lazy('IVA coopago'), max_digits=25, decimal_places=15, blank=True, null=True)
    coopago_bruto = models.DecimalField(_lazy('coopago bruto'), max_digits=25, decimal_places=15, blank=True, null=True)

    # Anulacion
    citas_anuladas = ArrayField(models.IntegerField(), blank=True, null=True)

    objects = DetalleFacturaManager()

    class Meta:
        verbose_name = 'detalle de factura'
        verbose_name_plural = 'detalles de factura'
    
    def __str__(self):
        return '{} - {}'.format(self.id, self.factura_id)

    @property
    def _cita(self):
        """Retorna una cita asociada al detalle."""

        if not self.factura.anulado_por:
            return self.citas.all()[0]

        Cita = import_string('agenda.models.Cita')
        return Cita.objects.get(id=self.citas_anuladas[0])
    
    @property
    def paciente(self):
        """Retorna el paciente asociado al detalle de la factura."""

        return self._cita.paciente
    
    @property
    def autorizacion(self):
        """Retorna el numero de autorizacion asociado al detalle de la factura."""

        return self._cita.autorizacion
    
    @property
    def servicio(self):
        """Retorna el servicio asociado al detalle de la factura."""

        return self._cita.servicio
    
    @property
    def fecha_atencion(self):
        return self._cita.inicio
    
    def _format_diagnostico(self, diagnostico):
        if diagnostico:
            return diagnostico['codigo']

        return ''

    @property
    def cie(self):
        with suppress(Exception):
            return self._format_diagnostico(self._cita.diagnostico['diagnosticoPrincipalItem'])
        
        return ''

    def subtotal(self):
        """Calcula el subtotal del detalle."""

        return max(self.cantidad * self.valor - self.coopago, 0)
