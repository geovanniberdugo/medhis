import graphene
from graphene_django_extras.base_types import CustomTime
from graphene_django_extras.utils import queryset_factory
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField 
)
from common.schema.fields import WithResolverDjangoListObjectField
from common.utils import in_query
from common.schema import User
from .. import models
from .. import filters

class Sucursal(DjangoObjectType):

    class Meta:
        model = models.Sucursal
        description = 'Una sucursal es una sede del cliente'

class SucursalList(DjangoListObjectType):

    class Meta:
        model = models.Sucursal
        description = 'Definición del tipo de una lista de sucursales'

class Institucion(DjangoObjectType):

    tipo_documento_display = graphene.String(source='get_tipo_documento_display')

    class Meta:
        model = models.Institucion
        description = 'Una institución es la empresa a nombre de la cual se realiza el servicio'

class InstitucionList(DjangoListObjectType):

    class Meta:
        model = models.Institucion
        description = 'Definición del tipo de una lista de instituciones'
        filter_fields = ['id']

class HorarioAtencion(DjangoObjectType):

    # TODO cambiar a enum
    dia = graphene.String(required=True, description='1-7. Lunes es 1. Domingo es 7.')
    horas_atencion = graphene.NonNull(
        graphene.List(graphene.NonNull(CustomTime)),
        source='espacios_atencion',
        description='Horas en las que atiende un medico según la duración de sus citas.',
        deprecation_reason='Usar horasAtencion en Medico'
    )

    class Meta:
        model = models.HorarioAtencion
        description = 'Horario de atención del medico'

class HorarioAtencionList(DjangoListObjectType):

    class Meta:
        model = models.HorarioAtencion
        filter_fields = ['medico', 'sucursal']
        description = 'Definición del tipo de una lista de horarios de atención'

class Empleado(DjangoObjectType):

    turnos = graphene.Int(source='turnos', deprecation_reason='Usar `atencionesSimultaneas`')

    instituciones = graphene.List(graphene.NonNull(Institucion))
    usuario = graphene.Field(User, source='usuario', required=True)
    sucursales = graphene.List(graphene.NonNull(Sucursal), source='sucursales')
    nombre_completo = graphene.String(source='__str__', description='Nombre completo del empleado')
    duracion = graphene.String(source='duracion', description='Duración de la atención de las citas')
    title = graphene.String(source='__str__', description='Nombre completo. Campo usado en fullCalendar')
    horarios_atencion = graphene.List(graphene.NonNull(HorarioAtencion), sucursal=graphene.ID(), fecha=graphene.Date())
    horas_atencion = graphene.NonNull(
        graphene.List(graphene.NonNull(CustomTime)),
        sucursal=graphene.ID(required=True), fecha=graphene.Date(required=True),
        description='Horas en las que atiende un medico según la duración de sus citas.'
    )

    class Meta:
        model = models.Empleado
        description = 'Un empleado de la IPS.'
    
    def resolve_firma(self, info, **kwargs):
        return self.firma.url if self.firma else ''
    
    def resolve_instituciones(self, info, **kwargs):
        return self.instituciones.all()
    
    def resolve_horarios_atencion(self, info, **kwargs):
        fecha = kwargs.get('fecha', None)
        sucursal = kwargs.get('sucursal', None)
        qs = queryset_factory(self.horarios_atencion.all(), info.field_asts, info.fragments, **kwargs)
        if sucursal:
            qs = qs.by_sucursal(sucursal)
        if fecha:
            qs = qs.by_fecha(fecha)
        return qs

    def resolve_horas_atencion(self, info, fecha, sucursal, **kwargs):
        return self.horas_atencion([fecha], sucursal)[fecha]


class EmpleadoList(DjangoListObjectType):

    class Meta:
        model = models.Empleado
        description = 'Definición del tipo de una lista de empleados'
        filterset_class = filters.EmpleadoFilter


class Query:
    empleados = DjangoListObjectField(EmpleadoList, description='Lista de todos los empleados')
    instituciones = DjangoListObjectField(InstitucionList, description='Lista de todas las instituciones')
    sucursales = DjangoListObjectField(SucursalList, description='Lista de todas las sucursales')

    institucion = DjangoObjectField(Institucion, description='Una sola institución')
    sucursal = DjangoObjectField(Sucursal, description='Una sola sucursal')
    empleado = DjangoObjectField(Empleado, description='Un solo Empleado')
