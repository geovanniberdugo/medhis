from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models

class CieSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo CIE."""

    class Meta:
        model = models.Cie
        fields = ['codigo', 'nombre'] + SelectableSerializerMixin.mixin_fields