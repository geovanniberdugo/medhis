from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from . import services as s
from . import models

class AnularFacturaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Factura
        fields = ['id', 'razon_anulacion']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        return s.anular_factura(instance, empleado=empleado, **validated_data)

class AnularReciboCajaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReciboCaja
        fields = ['id', 'razon_anulacion']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.anular(empleado=empleado, **validated_data)
        return instance

class ReciboCajaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ReciboCaja
        fields = ['id', 'servicio_prestado', 'forma_pago', 'valor', 'detalle', 'sucursal']
    
    def create(self, validated_data):
        empleado = self.context['request'].user.empleado
        return models.ReciboCaja.objects.generar(empleado=empleado, **validated_data)

class DetalleCajaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DetalleCaja
        fields = ['forma_pago', 'valor']

class CajaSerializer(serializers.ModelSerializer):

    detalles = DetalleCajaSerializer(many=True)

    class Meta:
        model = models.Caja
        fields = ['sucursal', 'pagos', 'detalles']
    
    def create(self, validated_data):
        empleado = self.context['request'].user.empleado
        return models.Caja.objects.cerrar(empleado=empleado, **validated_data)

class EditarCajaSerializer(serializers.ModelSerializer):

    detalles = DetalleCajaSerializer(many=True)

    class Meta:
        model = models.Caja
        fields = ['id', 'fecha', 'sucursal', 'pagos', 'detalles']

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance

class RecibirCajaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Caja
        fields = ['id']

    @transaction.atomic
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.recibido_por = empleado
        instance.recibido_at = timezone.now()
        instance.save()
        return instance

class VerificarCajaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Caja
        fields = ['id', 'verificacion_correcta', 'observaciones_verificacion']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance = instance.verificar(empleado=empleado, **validated_data)
        return instance

class DetalleFacturaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DetalleFactura
        fields = ['id', 'cantidad', 'valor', 'coopago', 'iva_coopago', 'coopago_bruto', 'citas']

class FacturaSerializer(serializers.ModelSerializer):

    detalle = DetalleFacturaSerializer(many=True)

    class Meta:
        model = models.Factura
        fields = [
            'id', 'numero', 'fecha_inicio', 'fecha_fin', 'cliente', 'paciente',
            'institucion', 'detalle', 'observaciones', 'fecha_expedicion'
        ]
    
    def validate(self, data):
        """Valida que si el cliente factura al paciente el paciente sea obligatorio."""

        if data['cliente'].factura_paciente and not data.get('paciente', None):
            raise serializers.ValidationError({
                'paciente': self.error_messages['required'],
            }, code='required')
        
        return data

    def create(self, validated_data):
        return models.Factura.objects.generar(**validated_data)
