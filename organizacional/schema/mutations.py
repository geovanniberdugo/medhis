import graphene
from graphene_file_upload.scalars import Upload
from graphene_django_extras import DjangoSerializerMutation, DjangoInputObjectType
from .. import serializers
from .. import models


class SucursalMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.SucursalSerializer
        input_field_name = 'input'

class InstitucionMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.InstitucionSerializer
        input_field_name = 'input'

class HorarioAtencionInput(DjangoInputObjectType):

    # TODO solucion rapida corregir enum
    dia = graphene.String(required=True)

    class Meta:
        model = models.HorarioAtencion
        exclude_fields = ['medico', 'sucursal']

class MedicoInput(DjangoInputObjectType):

    sucursal = graphene.ID(required=True)
    horarios = graphene.List(HorarioAtencionInput, required=True)

    class Meta:
        model = serializers.MedicoSerializer.Meta.model
        only_fields = serializers.MedicoSerializer.Meta.fields
        input_for = 'update'

class MedicoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.MedicoSerializer
        only_fields = serializers.MedicoSerializer.Meta.fields
        input_field_name = 'input'

class CrearEmpleadoAdministrativoInput(DjangoInputObjectType):

    rol = graphene.ID(required=True)
    username = graphene.String(required=True)
    password1 = graphene.String(required=True)
    password2 = graphene.String(required=True)

    class Meta:
        model = serializers.EmpleadoAdministrativoSerializer.Meta.model
        only_fields = serializers.EmpleadoAdministrativoSerializer.Meta.fields

class EditarEmpleadoAdministrativoInput(DjangoInputObjectType):

    password1 = graphene.String()
    password2 = graphene.String()
    rol = graphene.ID(required=True)
    username = graphene.String(required=True)

    class Meta:
        model = serializers.EmpleadoAdministrativoSerializer.Meta.model
        only_fields = serializers.EmpleadoAdministrativoSerializer.Meta.fields
        input_for = 'update'

class EmpleadoAdministrativoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.EmpleadoAdministrativoSerializer
        only_fields = serializers.EmpleadoAdministrativoSerializer.Meta.fields
        input_field_name = 'input'

class CrearMedicoInput(DjangoInputObjectType):

    firma = graphene.Field(Upload)
    rol = graphene.ID(required=True)
    duracion_cita = graphene.String()
    username = graphene.String(required=True)
    password1 = graphene.String(required=True)
    password2 = graphene.String(required=True)

    class Meta:
        model = serializers.MedicoSerializer2.Meta.model
        only_fields = serializers.MedicoSerializer2.Meta.fields

class EditarMedicoInput(DjangoInputObjectType):

    password1 = graphene.String()
    password2 = graphene.String()
    firma = graphene.Field(Upload)
    rol = graphene.ID(required=True)
    duracion_cita = graphene.String()
    username = graphene.String(required=True)

    class Meta:
        model = serializers.MedicoSerializer2.Meta.model
        only_fields = serializers.MedicoSerializer2.Meta.fields
        input_for = 'update'

class MedicoMutation2(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.MedicoSerializer2
        only_fields = serializers.MedicoSerializer2.Meta.fields
        input_field_name = 'input'

class Mutation:
    crear_medico = MedicoMutation2.CreateField(description='Crea un medico')
    editar_medico = MedicoMutation2.UpdateField(description='Edita un medico')
    crear_sucursal = SucursalMutation.CreateField(description='Crea una sucursal')
    editar_sucursal = SucursalMutation.UpdateField(description='Edita una sucursal')
    crear_institucion = InstitucionMutation.CreateField(description='Crea una institucion')
    editar_institucion = InstitucionMutation.UpdateField(description='Edita una institucion')
    guardar_horario_atencion = MedicoMutation.UpdateField(description='Guarda el horario de atención de un medico')
    crear_empleado_administrativo = EmpleadoAdministrativoMutation.CreateField(description='Crea un empleado administrativo')
    editar_empleado_administrativo = EmpleadoAdministrativoMutation.UpdateField(description='Edita un empleado administrativo')
