from graphene_django_extras import DjangoSerializerMutation
from .. import serializers


class ServicioMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.ServicioSerializer
        input_field_name = 'input'
        only_fields = serializers.ServicioSerializer.Meta.fields


class ClienteMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.ClienteSerializer
        input_field_name = 'input'
        only_fields = serializers.ClienteSerializer.Meta.fields


class PlanMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.PlanSerializer
        input_field_name = 'input'
        only_fields = serializers.PlanSerializer.Meta.fields

class TarifaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.TarifaSerializer
        input_field_name = 'input'
        only_fields = serializers.TarifaSerializer.Meta.fields

class Mutation:
    crear_servicio = ServicioMutation.CreateField(description='Crea un servicio')
    crear_cliente = ClienteMutation.CreateField(description='Crea un cliente')
    crear_tarifa = TarifaMutation.CreateField(description='Crea una tarifa')
    crear_plan = PlanMutation.CreateField(description='Crea un plan')

    editar_servicio = ServicioMutation.UpdateField(description='Edita un servicio')
    editar_cliente = ClienteMutation.UpdateField(description='Edita un cliente')
    editar_tarifa = TarifaMutation.UpdateField(description='Edita una tarifa')
    editar_plan = PlanMutation.UpdateField(description='Edita un plan')

    borrar_tarifa = TarifaMutation.DeleteField(description='Borra una tarifa')
