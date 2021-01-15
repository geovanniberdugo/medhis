import graphene
from graphene_file_upload.scalars import Upload
from graphene_django_extras.base_types import CustomDate
from graphene_django_extras import DjangoSerializerMutation, DjangoInputObjectType
from common.schema import LocalCustomDateTime
from .. import serializers
from .. import models

class NuevoPacienteInput(DjangoInputObjectType):

    foto = graphene.Field(Upload)
    firma = graphene.Field(Upload)
    opcion_llenado = graphene.String(required=True)
    
    class Meta:
        model = models.Paciente
        only_fields = serializers.PacienteSerializer2.Meta.fields

class EditarPacienteInput(DjangoInputObjectType):

    foto = graphene.Field(Upload)
    firma = graphene.Field(Upload)
    opcion_llenado = graphene.String(required=True)
    
    class Meta:
        input_for = 'update'
        model = models.Paciente
        only_fields = serializers.PacienteSerializer2.Meta.fields

class PacienteMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        serializer_class = serializers.PacienteSerializer2
        only_fields = serializers.PacienteSerializer2.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class AcompananteInput(DjangoInputObjectType):

    class Meta:
        model = models.Acompanante
        only_fields = serializers.AcompananteOrdenSerializer.Meta.fields
        description = 'Input para actualizar acompañante de la orden'

class OrdenInfoInput(DjangoInputObjectType):

    acompanante = graphene.InputField(AcompananteInput, description='acompañante')

    class Meta:
        model = serializers.OrdenInfoSerializer.Meta.model
        only_fields = serializers.OrdenInfoSerializer.Meta.fields
        input_for = 'update'

class OrdenInfoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.OrdenInfoSerializer
        input_field_name = 'input'
        only_fields = serializers.OrdenInfoSerializer.Meta.fields

class AddServicioOrdenInput(DjangoInputObjectType):

    autorizacion = graphene.String()
    fecha_autorizacion = CustomDate()
    medico = graphene.ID(required=True)
    sucursal = graphene.ID(required=True)
    duracion = graphene.String(required=True)
    fecha = LocalCustomDateTime(required=True)

    class Meta:
        model = serializers.AgregarServicioOrdenSerializer.Meta.model
        only_fields = serializers.AgregarServicioOrdenSerializer.Meta.fields

class AgregarServicioOrdenMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'servicio_realizar'
        serializer_class = serializers.AgregarServicioOrdenSerializer
        only_fields = serializers.AgregarServicioOrdenSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class EditarTratamientoInput(DjangoInputObjectType):

    class Meta:
        model = serializers.TratamientoSerializer.Meta.model
        only_fields = serializers.TratamientoSerializer.Meta.fields
        input_for = 'update'

class TratamientoMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'tratamiento'
        serializer_class = serializers.TratamientoSerializer
        only_fields = serializers.TratamientoSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class RecibirTratamientoTerminadoInput(DjangoInputObjectType):

    class Meta:
        model = serializers.RecibirTratamientoTerminadoSerializer.Meta.model
        only_fields = serializers.RecibirTratamientoTerminadoSerializer.Meta.fields
        input_for = 'update'

class RecibirTratamientoTerminadoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.RecibirTratamientoTerminadoSerializer
        input_field_name = 'input'
        only_fields = serializers.RecibirTratamientoTerminadoSerializer.Meta.fields
        output_field_name = 'servicio_realizar'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class VerificarTratamientoTerminadoInput(DjangoInputObjectType):

    class Meta:
        model = serializers.VerificarTratamientoTerminadoSerializer.Meta.model
        only_fields = serializers.VerificarTratamientoTerminadoSerializer.Meta.fields
        input_for = 'update'

class VerificarTratamientoTerminadoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.VerificarTratamientoTerminadoSerializer
        input_field_name = 'input'
        only_fields = serializers.VerificarTratamientoTerminadoSerializer.Meta.fields
        output_field_name = 'servicio_realizar'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class VerificarInicioTratamientoInput(DjangoInputObjectType):

    class Meta:
        model = serializers.VerificarInicioTratamientoSerializer.Meta.model
        only_fields = serializers.VerificarInicioTratamientoSerializer.Meta.fields
        input_for = 'update'

class VerificarInicioTratamientoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.VerificarInicioTratamientoSerializer
        input_field_name = 'input'
        only_fields = serializers.VerificarInicioTratamientoSerializer.Meta.fields
        output_field_name = 'servicio_realizar'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class VerificarInicioAdminTratamientoInput(DjangoInputObjectType):

    class Meta:
        model = serializers.VerificarInicioAdminTratamientoSerializer.Meta.model
        only_fields = serializers.VerificarInicioAdminTratamientoSerializer.Meta.fields
        input_for = 'update'

class VerificarInicioAdminTratamientoMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'servicio_realizar'
        serializer_class = serializers.VerificarInicioAdminTratamientoSerializer
        only_fields = serializers.VerificarInicioAdminTratamientoSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class ReagendarCitasInput(DjangoInputObjectType):

    class Meta:
        input_for = 'update'
        model = serializers.ReagendarCitasSerializer.Meta.model
        only_fields = serializers.ReagendarCitasSerializer.Meta.fields

class ReagendarCitasMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'servicio_realizar'
        serializer_class = serializers.ReagendarCitasSerializer
        only_fields = serializers.ReagendarCitasSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class Mutation:
    crear_paciente = PacienteMutation.CreateField(description='Crea un paciente')
    editar_paciente = PacienteMutation.UpdateField(description='Edita un paciente')
    editar_tratamiento = TratamientoMutation.UpdateField(description='Edita el tratamiento')
    editar_orden_info = OrdenInfoMutation.UpdateField(description='Edita los datos de la orden')
    agregar_servicio_orden = AgregarServicioOrdenMutation.CreateField(description='Agrega servicio a realizar a orden')
    recibir_tratamiento_terminado = RecibirTratamientoTerminadoMutation.UpdateField(description='Recibe el tratamiento terminado')
    verificar_tratamiento_terminado = VerificarTratamientoTerminadoMutation.UpdateField(description='Verifica el tratamiento terminado')
    reagendar_citas = ReagendarCitasMutation.UpdateField(description='Reagenda las citas excusadas, no atendidas y no asistio a otro horario')
    verificar_inicio_tratamiento = VerificarInicioTratamientoMutation.UpdateField(description='Verifica los datos de la orden al inicio de tratamiento')
    verificar_inicio_admin_tratamiento = VerificarInicioAdminTratamientoMutation.UpdateField(description='Verifica en el reporte de inicio de tratamiento')
