import graphene
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField 
)
from rest_framework.reverse import reverse
from common.schema.fields import WithResolverDjangoListObjectField
from common.schema import converter, LocalCustomDateTime
from common.utils import in_query
from pacientes.schema.queries import Paciente
from servicios.schema.queries import Plan, Servicio
from organizacional.schema import Institucion, Empleado, Sucursal
from .. import models
from .. import filters


class TipoAgenda(DjangoObjectType):

    class Meta:
        model = models.Agenda
        description = 'Los tipos de agenda agrupan los medicos que manejan un misma duración de una cita'

class TiposAgendaList(DjangoListObjectType):

    class Meta:
        model = models.Agenda
        description = 'Definición del tipo de una lista de tipos de agenda'

class HistorialEstado(DjangoObjectType):

    estado_label = graphene.String(source='estado_display', description='Nombre del estado')

    class Meta:
        model = models.HistorialEstado
        description = 'Historial de estados de una cita'

class Horario(graphene.ObjectType):

    id = graphene.ID(required=True)
    end = LocalCustomDateTime(required=True)
    start = LocalCustomDateTime(required=True)
    medico = graphene.Field(Empleado, required=True)
    sucursal = graphene.Field(Sucursal, required=True)
    resource_id = graphene.ID(description='Id del medico. Usado en fullCalendar')

    def resolve_resource_id(self, info, **kwargs):
        return self.medico.id

class Cita(DjangoObjectType):

    estado_display = graphene.String(description='Nombre del estado')
    cumplida = graphene.Boolean(description='Indica si la cita fue cumplida')
    convenio = graphene.Field(Plan, description='Convenio asociado a la cita')
    terminada = graphene.Boolean(description='Indica si la cita fue terminada')
    cancelada = graphene.Boolean(description='Indica si la cita fue cancelada')
    paciente = graphene.Field(Paciente, description='Paciente atendido en la cita')
    can_move = graphene.Boolean(description='Indica si la cita se pude reprogramar')
    servicio = graphene.Field(Servicio, description='Servicio a ser atendido en la cita')
    horario = graphene.Field(Horario, deprecation_reason='Usar campos directos de la cita')
    color = graphene.String(source='color', description='Color mostrado en el calendario segun el estado')    
    historial_actual = graphene.Field(HistorialEstado, description='Historial del estado actual de la cita')
    can_add_encuentro = graphene.Boolean(description='Indica si el usuario puede agregar encuentros a la cita')
    estados_disponibles = graphene.List(graphene.String, description='Indica los estados que puede tener la cita')

    redirecciona_url = graphene.String(source='redirecciona_url', description='URL a la cual se redirecciona cuando la cita se cumple')
    valor_pagar_medico = graphene.Float(source='valor_pagar_medico', description='Valor que se le debe pagar al medico por la cita')
    can_change_estado = graphene.Boolean(description='Indica si el usuario tiene permiso de cambiar el estado de la cita')
    institucion = graphene.Field(Institucion, source='institucion', description='IPS que factura la cita')
    can_edit = graphene.Boolean(description='Indica si el usuario puede editar la sesión')
    visita_url = graphene.String(description='URL de la visita asociada a la cita')
    orden_url = graphene.String(description='URL de la orden asociada a la cita')

    category = graphene.String(source='estado_display', description='Estado de la cita. Usada en fullCalendar')
    title = graphene.String(description='Nombre del paciente. Usado en fullCalendar')
    resource_id = graphene.ID(description='Id del medico. Usado en fullCalendar')
    redirecciona_link = graphene.String(deprecation_reason='usar redireccionaUrl')
    end = LocalCustomDateTime(source='end', description='Fecha y hora de finalización de la cita', deprecation_reason='Usar fin')
    start = LocalCustomDateTime(source='start', description='Fecha y hora de inicio de la cita', deprecation_reason='Usar inicio')
    empresa = graphene.Field(Plan, source='empresa', description='Convenio asociado a la cita', deprecation_reason='Usar convenio')
    estado_actual = graphene.String(source='estado_actual', description='Estado actual de la cita', deprecation_reason='Usar historial estado')
    estado_actual_label = graphene.String(source='estado_display', description='Nombre del estado', deprecation_reason='Usar historial estado')

    class Meta:
        model = models.Cita
    
    def resolve_horario(self, info, **kwargs):
        return Horario(
            id=self.id,
            end=self.fin,
            start=self.inicio,
            medico=self.medico,
            sucursal=self.sucursal
        )
    
    def resolve_can_change_estado(self, info, **kwargs):
        return self.can_change_estado(info.context.user)

    def resolve_orden_url(self, info, **kwargs):
        return self.orden_url(info.context.user)
    
    def resolve_visita_url(self, info, **kwargs):
        return self.visita_url(info.context.user)
    
    def resolve_title(self, info, **kwargs):
        return str(self.paciente)
    
    def resolve_resource_id(self, info, **kwargs):
        return self.medico_id

    def resolve_redirecciona_url(self, info, **kwargs):
        return self.redirecciona_url()

    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)

    def resolve_estado_display(self, info, **kwargs):
        return info.context.dataloaders.estado_display_by_cita.load(self.id)

    def resolve_medico(self, info, **kwargs):
        return info.context.dataloaders.medico_by_cita.load(self.id)

    def resolve_servicio_prestado(self, info, **kwargs):
        return info.context.dataloaders.tratamiento_by_cita.load(self.id)

    def resolve_sucursal(self, info, **kwargs):
        return info.context.dataloaders.sucursal_by_cita.load(self.id)

    def resolve_servicio(self, info, **kwargs):
        return info.context.dataloaders.servicio_by_cita.load(self.id)
    
    def resolve_can_move(self, info, **kwargs):
        return info.context.dataloaders.can_move_by_cita.load(self.id)

    def resolve_convenio(self, info, **kwargs):
        return info.context.dataloaders.convenio_by_cita.load(self.id)

    def resolve_paciente(self, info, **kwargs):
        return info.context.dataloaders.paciente_by_cita.load(self.id)

    def resolve_historial_actual(self, info, **kwargs):
        return info.context.dataloaders.historial_actual_by_cita.load(self.id)
    
    def resolve_cumplida(self, info, **kwargs):
        return info.context.dataloaders.cumplida_by_cita.load(self.id)

    def resolve_terminada(self, info, **kwargs):
        return info.context.dataloaders.terminada_by_cita.load(self.id)

    def resolve_cancelada(self, info, **kwargs):
        return info.context.dataloaders.cancelada_by_cita.load(self.id)

    def resolve_encuentros(self, info, **kwargs):
        return info.context.dataloaders.encuentros_by_cita.load(self.id)

    def resolve_estados_disponibles(self, info, **kwargs):
        info.context.dataloaders.estados_disponibles_by_cita.user = info.context.user
        return info.context.dataloaders.estados_disponibles_by_cita.load(self.id)

    def resolve_can_add_encuentro(self, info, **kwargs):
        info.context.dataloaders.can_add_encuentro_by_cita.user = info.context.user
        return info.context.dataloaders.can_add_encuentro_by_cita.load(self.id)

    def resolve_detalle_factura(self, info, **kwargs):
        return info.context.dataloaders.detalle_factura_by_cita.load(self.id)

class CitaList(DjangoListObjectType):

    class Meta:
        model = models.Cita
        description = 'Definición del tipo de una lista de citas'
        filterset_class = filters.CitaFilter

class Query:
    tipos_agenda = DjangoListObjectField(TiposAgendaList, description='Lista todos los tipos de agenda')
    citas = WithResolverDjangoListObjectField(CitaList, description='Lista todas las citas')
    tipo_agenda = DjangoObjectField(TipoAgenda, description='Un solo tipo de agenda')

    cita = DjangoObjectField(Cita, description='Una sola cita')

    def resolve_citas(self, info, **kwargs):
        selectable = []
        prefetched = []

        if in_query('color', info):
            prefetched.append('estados')

        if in_query('institucion', info):
            selectable.append('servicio_prestado__orden__institucion')

        if in_query('title', info):
            selectable.append('servicio_prestado__orden__paciente')

        citas = models.Cita.objects.all()
        if len(selectable) > 0:
            citas = citas.select_related(*selectable)

        if len(prefetched) > 0:
            citas = citas.prefetch_related(*prefetched)

        return citas
