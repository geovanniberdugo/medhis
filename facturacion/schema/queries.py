import graphene
from contextlib import suppress
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoListObjectField, DjangoObjectField
)
from common.schema import LocalCustomDateTime
from organizacional.models import Institucion
from organizacional.schema import Sucursal
from pacientes.schema import Paciente
from .. import models
from .. import filters
from .. import utils


class ReciboCaja(DjangoObjectType):

    paciente = graphene.Field(Paciente)
    sucursal = graphene.Field(Sucursal)
    forma_pago_label = graphene.String(source='get_forma_pago_display')
    detalle_url = graphene.String(source='get_absolute_url', description='URL del recibo')
    can_anular = graphene.Boolean(description='Indica si se puede anular el recibo de caja')

    class Meta:
        model = models.ReciboCaja
        description = 'Pagos hechos por los pacientes.'
    
    def resolve_can_anular(self, info, **kwargs):
        return self.can_anular(info.context.user)
    
    def resolve_sucursal(self, info, **kwargs):
        return info.context.dataloaders.sucursal_by_recibo_caja.load(self.id)

    def resolve_paciente(self, info, **kwargs):
        return info.context.dataloaders.paciente_by_recibo_caja.load(self.id)

class ReciboCajaList(DjangoListObjectType):

    class Meta:
        model = models.ReciboCaja
        description = 'Lista de recibos de caja'
        filterset_class = filters.ReciboCajaFilter

class Caja(DjangoObjectType):

    total = graphene.Float(source='total', description='Valor total de la caja')
    can_edit = graphene.Boolean(description='Indica si se puede editar la caja')
    detalle_url = graphene.String(source='get_absolute_url', description='URL de la caja')

    class Meta:
        model = models.Caja
    
    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)

class CajaList(DjangoListObjectType):

    class Meta:
        model = models.Caja
        description = 'Lista de cajas'
        filterset_class = filters.CajaFilter

class DetalleCaja(DjangoObjectType):

    forma_pago_label = graphene.String(source='get_forma_pago_display')

    class Meta:
        model = models.DetalleCaja

class Factura(DjangoObjectType):

    total = graphene.Float(description='Total de la factura')
    can_anular = graphene.Boolean(description='Indica si se puede anular la factura')
    detalle_url = graphene.String(source='get_absolute_url', description='URL de la factura')
    can_eliminar = graphene.Boolean(description='Indica si puede eliminar la factura del sistema')

    class Meta:
        model = models.Factura
        description = 'Factura generada'
    
    def resolve_can_anular(self, info, **kwargs):
        return self.can_anular(info.context.user)

    def resolve_can_eliminar(self, info, **kwargs):
        return self.can_eliminar(info.context.user)

    def resolve_total(self, info, **kwargs):
        return info.context.dataloaders.total_by_factura.load(self.id)

class FacturaList(DjangoListObjectType):

    class Meta:
        model = models.Factura
        description = 'Lista de facturas'
        filterset_class = filters.FacturaFilter

class DetalleFactura(DjangoObjectType):

    subtotal = graphene.Float(source='subtotal')
    fecha_atencion = LocalCustomDateTime(description='Fecha de atencion de la primera cita')

    class Meta:
        model = models.DetalleFactura
        description = 'Detalle de una factura generada.'


class Query:
    recibos_caja = DjangoListObjectField(ReciboCajaList, description='Todos los recibos de caja')
    recibo_caja = DjangoObjectField(ReciboCaja, description='Un solo recibo de caja')
    facturas = DjangoListObjectField(FacturaList, description='Todos las facturas')
    cajas = DjangoListObjectField(CajaList, description='Todos las cajas')
    caja = DjangoObjectField(Caja, description='Un sola caja')

    consecutivo_factura = graphene.Int(ips=graphene.ID(required=True), description='Consecutivo de la factura')

    def resolve_consecutivo_factura(self, info, ips, **kwargs):
        with suppress(Exception):
            institucion = Institucion.objects.get(id=ips)
            return utils.consecutivo_factura(institucion)
        return None
