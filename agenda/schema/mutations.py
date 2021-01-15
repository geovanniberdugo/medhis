import graphene
from django.db import transaction
from graphene_django_extras import DjangoSerializerMutation, DjangoInputObjectType
from graphene_django_extras.registry import get_global_registry
from graphene_django_extras.utils import get_Object_or_None
from common.schema import converter
from .. import serializers
from .. import models
from .queries import Cita


class PacienteCitaInput(DjangoInputObjectType):

    class Meta:
        model = serializers.PacienteSerializer.Meta.model
        only_fields = serializers.PacienteSerializer.Meta.fields
        description = 'Input para agregar paciente a la cita.'


class AgendarCitaInput(DjangoInputObjectType):

    estado = graphene.String(required=True)
    duracion = graphene.String(required=True)
    servicio = graphene.ID(required=True, description='Id del servicio')
    convenio = graphene.ID(required=True, description='Id del convenio')
    institucion = graphene.ID(required=True, description='Id de la institucion')
    paciente = graphene.InputField(PacienteCitaInput, required=True, description='paciente')

    class Meta:
        model = serializers.AgendarCitaSerializar.Meta.model
        only_fields = serializers.AgendarCitaSerializar.Meta.fields
        description = 'Input para agendar una cita'


class AgendarCitaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.AgendarCitaSerializar
        input_field_name = 'input'
        only_fields = serializers.AgendarCitaSerializar.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}
    
    @classmethod
    def perform_mutate(cls, obj, info):
        if obj.redirecciona_url():
            info.context.session['cita'] = obj.id
        return super().perform_mutate(obj, info)


class MoverCitaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.MoverCitaSerializer
        input_field_name = 'input'
        only_fields = serializers.MoverCitaSerializer.Meta.fields


class AgregarAutorizacionCitaInput(DjangoInputObjectType):

    class Meta:
        input_for = 'update'
        description = 'Input para agregar autorizacion a una cita'
        model = serializers.AddAutorizacionCitaSerializer.Meta.model
        only_fields = serializers.AddAutorizacionCitaSerializer.Meta.fields


class AgregarAutorizacionCitaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.AddAutorizacionCitaSerializer
        input_field_name = 'input'


class TipoAgendaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.TipoAgendaSerializer
        input_field_name = 'input'
        output_field_name = 'tipo_agenda'


class EstadoCitaInput(DjangoInputObjectType):

    motivo = graphene.String(description='Motivo de cancelación de la cita')
    reagendar = graphene.Boolean(description='Indica si se debe reagendar citas')
    estado = graphene.String(required=True, description='Nuevo estado de la cita')

    class Meta:
        input_for = 'update'
        description = 'Input para actualizar el estado de una cita'
        model = serializers.ActualizarEstadoCitaSerializer.Meta.model
        only_fields = serializers.ActualizarEstadoCitaSerializer.Meta.fields


class ActualizarEstadoCitaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.ActualizarEstadoCitaSerializer
        input_field_name = 'input'
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}


class TerminarVisitaMutation(graphene.Mutation):
    """Permite marcar la cita como terminada."""

    cita = graphene.Field(Cita)

    class Arguments:
        id = graphene.ID(required=True, description='ID de la cita')
    
    @classmethod
    def mutate(cls, root, info, id):
        empleado = info.context.user.empleado
        cita = get_Object_or_None(models.Cita, pk=id)

        cita.terminar_cita(empleado)
        return cls(cita=cita)

class CambiarMotivoEstadoCita(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'historial_estado'
        serializer_class = serializers.CambiarMotivoEstadoCita
        only_fields = serializers.CambiarMotivoEstadoCita.Meta.fields

class Mutation:
    agendar_cita = AgendarCitaMutation.CreateField(description='Agendar cita')
    mover_cita = MoverCitaMutation.UpdateField(description='Mover cita a un nuevo horario')
    agregar_autorizacion_cita = AgregarAutorizacionCitaMutation.UpdateField(description='Agrega o edita la autorizacion de una cita')

    crear_tipo_agenda = TipoAgendaMutation.CreateField(description='Crea un tipo de agenda')
    editar_tipo_agenda = TipoAgendaMutation.UpdateField(description='Edita un tipo de agenda')

    actualizar_estado_cita = ActualizarEstadoCitaMutation.UpdateField(description='Actualiza el estado de la cita')
    terminar_visita = TerminarVisitaMutation.Field(description='Marca una cita como terminada')
    cambiar_motivo_estado_cita = CambiarMotivoEstadoCita.UpdateField(description='Cambiar el motivo de no cumplimiento de una cita')
