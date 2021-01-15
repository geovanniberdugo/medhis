from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models


class ServicioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo servicio."""

    class Meta:
        model = models.Servicio
        fields = ['id', 'nombre', 'codigo', 'abreviatura', 'cups', 'tipo']

class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo cliente."""

    class Meta:
        model = models.Cliente
        fields = [
            'id','nombre', 'razon_social', 'nit', 'direccion', 'telefono', 'discriminar_iva',
            'codigo', 'ciudad', 'sesiones_autorizacion', 'factura_paciente', 'puc_facturacion',
            'tipo'
        ]


class PlanSerializer(serializers.ModelSerializer):
    """Serializer para el modelo plan."""

    class Meta:
        model = models.Plan
        fields = ['id', 'nombre', 'cliente']


class TarifaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Tarifa."""

    class Meta:
        model = models.Tarifa
        fields = ['id', 'institucion', 'plan', 'servicio', 'valor', 'coopago', 'iva_coopago']

class TarifaClienteSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para las tarifas"""

    class Meta:
        model = models.Tarifa
        fields = SelectableSerializerMixin.mixin_fields + ['valor']
    
    def get_label(self, obj):
        return str(obj.servicio)
    
    def get_value(self, obj):
        return obj.servicio.pk
