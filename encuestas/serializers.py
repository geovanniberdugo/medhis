from rest_framework import serializers
from . import models


class SatisfaccionGlobalSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SatisfaccionGlobal."""

    class Meta:
        model = models.SatisfaccionGlobal
        fields = ['id', 'paciente', 'fecha', 'pregunta1', 'pregunta2']

class EventoAdversoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo EventosAdversos."""

    class Meta:
        model = models.EventoAdverso
        fields = [
            'id', 'paciente', 'fecha', 'caida', 'tipo_caida', 'medicamentos'
        ]