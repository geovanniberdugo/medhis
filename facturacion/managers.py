from sequences import get_next_value
from django.db import models, transaction
from .utils import update_consecutivo_factura

class ReciboCajaQuerySet(models.QuerySet):

    def by_fecha(self, fecha):
        """Filtra los recibos de caja por fecha."""

        return self.filter(fecha=fecha)

    def by_sucursal(self, sucursal):
        """Filtra los recibos de caja de la sucursal ingresada."""

        return self.filter(sucursal=sucursal).distinct()
    
    def by_caja(self, caja):
        """Filtra los recibos segun la fecha y sucursal de la caja."""

        return self.by_sucursal(caja.sucursal).by_fecha(caja.fecha)
    
    def by_documento_paciente(self, documento):
        """Filtra los recibos segun el numero de documento del paciente."""

        return self.filter(servicio_prestado__orden__paciente__numero_documento=documento)

    def by_paciente(self, paciente):
        """Filtra los recibos segun el paciente."""

        return self.filter(servicio_prestado__orden__paciente=paciente)
    
    def by_institucion(self, institucion):
        """Filtra los recibos de una institución especifica."""

        return self.filter(servicio_prestado__orden__institucion=institucion).distinct()
    
    def by_cliente(self, cliente):
        """Filtra los recibos de caja por cliente"""

        return self.filter(servicio_prestado__orden__plan__cliente=cliente)
    
    def fecha_entre(self, desde, hasta):
        """Filtra los recibos en el rango de fechas indicado (las fechas son incluyentes)."""

        return self.filter(fecha__gte=desde, fecha__lte=hasta)
    
    def anulados(self):
        return self.filter(anulado_por__isnull=False)

    def no_anulados(self):
        return self.filter(anulado_por__isnull=True)

class ReciboCajaManager(models.Manager.from_queryset(ReciboCajaQuerySet)):
    """Manager personalizado para el modelo ReciboCaja."""

    @transaction.atomic
    def generar(self, empleado, **kwargs):
        """Genera un nuevo recibo de caja."""

        return self.create(
            empleado=empleado,
            numero=get_next_value(self.model.nombre_consecutivo()),
            **kwargs
        )

class CajaQuerySet(models.QuerySet):

    def by_user(self, user):
        """
        Filtra las cajas según los permisos del usuario ingresado.

        :param user: Usuario.
        """

        if user.has_perm('facturacion.can_see_todas_cajas'):
            return self.all()

        return self.filter(empleado__usuario=user)
    
    def recibidas(self):
        """Un queryset con las cajas recibidas."""

        return self.filter(recibido_por__isnull=False)
    
    def no_recibidas(self):
        """Un queryset con las cajas que no han sido recibidas."""

        return self.exclude(id__in=self.recibidas())
    
    def verificadas(self):
        """Un queryset con las cajas verificadas por contabilidad."""

        return self.filter(verificado_por__isnull=False)
    
    def no_verificadas(self):
        """Un queryset con las cajas que no han sido verificadas por contabilidad."""

        return self.exclude(id__in=self.verificadas())

class CajaManager(models.Manager.from_queryset(CajaQuerySet)):

    @transaction.atomic
    def cerrar(self, empleado, detalles, **kwargs):
        """Cierra una caja."""

        caja = self.model.objects.create(empleado=empleado, **kwargs)
        
        DetalleCaja = caja.detalles.model
        list(map(lambda o: DetalleCaja.objects.create(caja=caja, **o), detalles))
        return caja

class FacturaQuerySet(models.QuerySet):
    
    def periodo_facturado(self, desde, hasta):
        """Un queryset con las facturas donde el periodo facturado sea el ingresado."""
        
        return self.filter(fecha_inicio=desde, fecha_fin=hasta)
    
    def fecha_expedicion_entre(self, desde, hasta):
        """Un queryset con las facturas creadas entre el rango de fecha ingresado."""

        return self.filter(fecha_expedicion__date__range=(desde, hasta))

    def institucion(self, institucion):
        """Un queryset con las facturas de la institucion ingresada."""

        return self.filter(institucion=institucion)
    
    def cliente(self, cliente):
        """Un queryset con las facturas asociadas al cliente ingresado."""

        return self.filter(cliente=cliente)

    def anulados(self):
        return self.filter(anulado_por__isnull=False)

    def no_anulados(self):
        return self.filter(anulado_por__isnull=True)

class FacturaManager(models.Manager.from_queryset(FacturaQuerySet)):
    """Manager personalizado para el modelo Factura."""
    
    @transaction.atomic
    def generar(self, numero, institucion, detalle, **kwargs):
        """Genera una nueva factura y la guarda en la base de datos."""

        factura = self.model.objects.create(
            institucion=institucion,
            numero=numero,
            **kwargs
        )

        update_consecutivo_factura(institucion, numero)

        DetalleFactura = factura.detalle.model
        list(map(lambda o: DetalleFactura.objects.crear(factura, **o), detalle))
        return factura

class DetalleFacturaManager(models.Manager):
    """Manager personalizado para el modelo DetalleFactura."""

    def crear(self, factura, citas, **kwargs):
        """Crea el detalle de una factura."""

        detalle = self.model.objects.create(factura=factura, **kwargs)
        detalle.citas = citas
        return detalle

class ParametroFacturaSiigoQuerySet(models.QuerySet):
    
    def by_factura(self, factura):
        tipo_servicio = factura.detalles.first().servicio.tipo
        return self.filter(tipo_cliente=factura.cliente.tipo, tipo_servicio=tipo_servicio).first()

class ParametroFacturaSiigoManager(models.Manager.from_queryset(ParametroFacturaSiigoQuerySet)):
    pass
