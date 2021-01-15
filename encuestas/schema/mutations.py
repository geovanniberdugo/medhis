from graphene_django_extras import DjangoSerializerMutation
from .. import serializers

class SatisfaccionGlobalMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.SatisfaccionGlobalSerializer
        input_field_name = 'input'
        output_field_name = 'satisfaccion_global'


class EventoAdversoMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.EventoAdversoSerializer
        input_field_name = 'input'
        output_field_name = 'evento_adverso'


class Mutation:
    crear_satisfaccion_global = SatisfaccionGlobalMutation.CreateField(description='Crea un registro de encuesta de satisfaccion global')
    crear_evento_adverso = EventoAdversoMutation.CreateField(description='Crea un registro de evento adverso para la encuesta')
