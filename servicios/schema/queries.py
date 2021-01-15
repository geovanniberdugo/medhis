import graphene
from django.urls import reverse
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField 
)
from organizacional.schema.queries import Institucion
from common.schema.fields import WithResolverDjangoListObjectField
from common.utils import in_query
from .. import models
from .. import filters

class Servicio(DjangoObjectType):

    clase = graphene.String(source='clase', description='Clase del servicio.')
    tipo_rips = graphene.String(source='tipo_rips', description='Tipo de RIPS que genera el servicio.')
    tarifas = graphene.NonNull(
        graphene.List(graphene.NonNull('servicios.schema.Tarifa')),
        plan=graphene.ID(), institucion=graphene.ID(),
    )
    
    class Meta:
        model = models.Servicio
        description = 'Un servicio es el producto que ofrecen las IPS.'
    
    def resolve_tarifas(self, info, plan=None, institucion=None, **kwargs):
        info.context.dataloaders.tarifas_by_servicio.plan = plan
        info.context.dataloaders.tarifas_by_servicio.institucion = institucion
        return info.context.dataloaders.tarifas_by_servicio.load(self.id)

class ServicioList(DjangoListObjectType):

    class Meta:
        model = models.Servicio
        description = 'Definición del tipo de una lista de servicios.'
        filterset_class = filters.ServicioFilter

class Tipo(DjangoObjectType):

    class Meta:
        model = models.Tipo
        description = 'Un tipo se usa para clasificar los servicios en categorias.'

class TipoList(DjangoListObjectType):

    class Meta:
        model = models.Tipo
        description = 'Definición del tipo para una lista de tipos.'

class Cliente(DjangoObjectType):

    instituciones = graphene.List(Institucion)
    tipo_display = graphene.String(required=True, source='tipo_display')
    planes_url = graphene.String(name='planesURL', description="URL para la vista de los planes del cliente")

    class Meta:
        model = models.Cliente
        description = 'Un cliente es la empresa a la cual se le facturan los servicios prestados'
    
    def resolve_planes_url(self, info, **kwargs):
        return reverse('servicios:listar-planes', args=(self.id, ))
    
    def resolve_instituciones(self, info, *kwargs):
        return self.instituciones.all()

class ClienteList(DjangoListObjectType):

    class Meta:
        model = models.Cliente
        description = 'Definición del tipo para una lista de clientes.'

class Plan(DjangoObjectType):

    nombre_completo = graphene.String(description='Nombre del plan en conjunto con el del cliente')
    requiere_autorizacion = graphene.Boolean(source='requiere_autorizacion', description='Indica si el convenio requiere autorización')

    class Meta:
        model = models.Plan
        description = 'Un plan son los distintos polizas que maneja un cliente'
    
    def resolve_nombre_completo(self, info, **kwargs):
        return info.context.dataloaders.nombre_completo_by_plan.load(self.id)
    
    def resolve_cliente(self, info, **kwargs):
        return info.context.dataloaders.cliente_by_plan.load(self.id)

class PlanList(DjangoListObjectType):

    class Meta:
        model = models.Plan
        description = 'Definición del tipo de una lista de planes'
        filterset_class = filters.PlanFilter

class Tarifa(DjangoObjectType):

    class Meta:
        model = models.Tarifa
        description = 'Una tarifa es el valor que se cobra por un servicio a un cliente'
        filter_fields = ['plan', 'institucion']

class TarifaList(DjangoListObjectType):

    class Meta:
        model = models.Tarifa
        description = 'Lista de tarifas'
        filter_fields = ['institucion', 'plan']

class Query:
    servicios = DjangoListObjectField(ServicioList, description='Lista todos los servicios')
    clientes = DjangoListObjectField(ClienteList, description='Lista todos los clientes')
    tarifas = DjangoListObjectField(TarifaList, description='Lista todas las tarifas')
    planes = DjangoListObjectField(PlanList, description='Lista todos los planes')
    tipos = DjangoListObjectField(TipoList, description='Lista todos los tipos')

    servicio = DjangoObjectField(Servicio, description='Un solo servicio')
    cliente = DjangoObjectField(Cliente, description='Un solo cliente')
    tarifa = DjangoObjectField(Tarifa, description='Una sola tarifa')
    plan = DjangoObjectField(Plan, description='Un solo plan')
