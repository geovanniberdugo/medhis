import graphene
from graphene_django_extras import DjangoSerializerMutation
from graphene_django_extras.utils import get_Object_or_None
from .. import serializers
from .. import models


class AbrirHistoriaMutation(graphene.Mutation):
    """Permite abrir historia."""

    historia = graphene.Field('historias.schema.Historia')

    class Arguments:
        id = graphene.ID(required=True, description='ID de la historia')

    @classmethod
    def mutate(cls, root, info, id):
        historia = get_Object_or_None(models.Historia, pk=id)

        historia.abrir()
        return cls(historia=historia)

class EncuentroMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.HistoriaSerializer
        input_field_name = 'input'
        only_fields = serializers.HistoriaSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}


class Mutation:
    abrir_historia = AbrirHistoriaMutation.Field(description='Abre una historia')
    crear_encuentro = EncuentroMutation.CreateField(description='Crea un encuentro')
    editar_encuentro = EncuentroMutation.UpdateField(description='Edita un encuentro')
    borrar_encuentro = EncuentroMutation.DeleteField(description='Borra un encuentro')
