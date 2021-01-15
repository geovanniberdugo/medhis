from rest_framework import serializers
from django.contrib.auth.models import Group
from common.serializers import SelectableSerializerMixin
from . import models

class InstitucionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo institucion."""

    class Meta:
        model = models.Institucion
        fields = [
            'id', 'nombre', 'razon_social', 'codigo', 'direccion',
            'telefono', 'ciudad', 'tipo_documento', 'identificacion'
        ]

class SucursalSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Sucursal."""

    class Meta:
        model = models.Sucursal
        fields = ['id', 'nombre', 'telefono', 'direccion', 'codigo_contable_recibo']

class EmpleadoAdministrativoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo empleado."""

    ERROR_MESSAGES = {
        'missmatch': 'Las contraseñas deben coincidir'
    }

    username = serializers.CharField()
    password1 = serializers.CharField(required=False)
    password2 = serializers.CharField(required=False)
    rol = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = models.Empleado
        fields = [
            'id', 'nombres', 'apellidos', 'cedula', 'activo',
            'username', 'password1', 'password2', 'rol'
        ]
    
    def validate(self, data):
        """Valida que las contraseñas sean iguales."""

        pass1 = data.get('password1', None)
        pass2 = data.get('password2', None)
        
        if pass1 != pass2:
            raise serializers.ValidationError({
                'password2': self.ERROR_MESSAGES['missmatch'],
            }, code='missmatch')

        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        return models.Empleado.objects.crear_empleado_administrativo(password=password, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password1', None)
        instance.update(password=password, **validated_data)
        return instance

class HorarioAtencionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HorarioAtencion
        fields = [
            'dia', 'inicio', 'fin', 'con_descanso', 'inicio_descanso', 'fin_descanso'
        ]

class MedicoSerializer(serializers.ModelSerializer):

    horarios = HorarioAtencionSerializer(many=True)
    sucursal = serializers.PrimaryKeyRelatedField(queryset=models.Sucursal.objects.all())

    class Meta:
        model = models.Empleado
        fields = ['id', 'sucursal', 'horarios', 'firma']
    
    def update(self, instance, validated_data):
        instance.guardar_horarios(sucursal=validated_data['sucursal'], horarios=validated_data['horarios'])
        return instance

class MedicoSerializer2(serializers.ModelSerializer):

    ERROR_MESSAGES = {
        'missmatch': 'Las contraseñas deben coincidir'
    }

    username = serializers.CharField()
    password1 = serializers.CharField(required=False)
    password2 = serializers.CharField(required=False)
    rol = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = models.Empleado
        fields = [
            'id', 'nombres', 'apellidos', 'cedula', 'activo', 'registro_medico', 'duracion_cita', 'atenciones_simultaneas',
            'username', 'password1', 'password2', 'rol', 'agenda', 'instituciones', 'porcentaje_pago', 'firma'
        ]
    
    def validate(self, data):
        """Valida que las contraseñas sean iguales."""

        pass1 = data.get('password1', None)
        pass2 = data.get('password2', None)
        print('..................................')
        print(data)

        if pass1 != pass2:
            raise serializers.ValidationError({
                'password2': self.ERROR_MESSAGES['missmatch'],
            }, code='missmatch')

        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        return models.Empleado.objects.crear_medico(password=password, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password1', None)
        instance.update(password=password, **validated_data)
        return instance
