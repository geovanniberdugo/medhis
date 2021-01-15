from datetime import datetime
from django.db import transaction
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from organizacional.models import Empleado, Sucursal
from agenda.models import Cita
from . import models


class PacienteSerializer2(serializers.ModelSerializer):

    FULL = 'full'
    NOEDIT = 'noedit'
    PARTIAL = 'partial'
    opcion_llenado = serializers.ChoiceField(choices=[FULL, NOEDIT, PARTIAL])

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento', 'genero',
            'numero_documento', 'estado_civil', 'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email',
            'grupo_sanguineo', 'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia', 'foto', 'firma',
            'activo', 'procedencia', 'parentesco_responsable', 'nombre_responsable', 'direccion_responsable',
            'telefono_responsable', 'identificacion_padre', 'nombre_padre', 'telefono_padre', 'identificacion_madre',
            'nombre_madre', 'telefono_madre', 'opcion_llenado', 'telefono2', 'empresa', 'direccion_empresa',
            'telefono_empresa'
        ]
        extra_kwargs = {
            'direccion': {'required': True}
        }
    
    def validate(self, data):
        """Valida que los datos del padre o madre sean obligatorios si el paciente es menor de edad."""

        if self.instance:
            self.instance.fecha_nacimiento = data.get('fecha_nacimiento', self.instance.fecha_nacimiento)
            if self.instance.is_menor_edad:
                if 'identificacion_padre' not in data and 'identificacion_madre' not in data:
                    raise serializers.ValidationError({
                        'identificacion_padre': self.error_messages['required'],
                        'identificacion_madre': self.error_messages['required'],
                    })
        return data
    
    def create(self, validated_data):
        return models.Paciente.objects.create(fecha_ingreso=datetime.today(), **validated_data)
    
    def update(self, instance, validated_data):
        llenado = validated_data.get('opcion_llenado')
        instance = super().update(instance, validated_data)
        if llenado == self.FULL and not instance.fecha_ingreso:
            instance.fecha_ingreso = datetime.today()
            instance.save()

        return instance

class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    graph_id = serializers.SerializerMethodField()
    edit_link = serializers.SerializerMethodField()
    citas_url = serializers.SerializerMethodField()
    pagos_url = serializers.SerializerMethodField()
    historias_link = serializers.SerializerMethodField()
    tratamientos_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento',
            'numero_documento', 'genero', 'estado_civil', 'fecha_nacimiento', 'zona', 'direccion', 'telefono',
            'celular', 'email', 'grupo_sanguineo', 'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia',
            'activo', 'fecha_ingreso', 'procedencia', 'parentesco_responsable', 'nombre_responsable', 'direccion_responsable', 'telefono_responsable',
            'edit_link', 'identificacion_padre', 'nombre_padre', 'telefono_padre', 'identificacion_madre', 'tratamientos_url',
            'nombre_madre', 'telefono_madre', 'foto', 'firma', 'graph_id', 'historias_link', 'citas_url', 'pagos_url'
        ]
        extra_kwargs = {
            'parentesco_responsable': {'required': True},
            'direccion_responsable': {'required': True},
            'nombre_responsable': {'required': True},
            'lugar_nacimiento': {'required': True},
            'lugar_residencia': {'required': True},
            'fecha_ingreso': {'required': True},
            'estado_civil': {'required': True},
            'direccion': {'required': True},
            'email': {'required': True},
            'zona': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = models.Paciente.URBANO
        self.fields['grupo_etnico'].initial = models.Paciente.OTRO
        self.fields['foto'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})
        self.fields['firma'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})
    
    def validate(self, data):
        """Valida que los datos del padre o madre sean obligatorios si el paciente es menor de edad."""

        if self.instance and self.instance.is_menor_edad:
            if 'identificacion_padre' not in data and 'identificacion_madre' not in data:
                raise serializers.ValidationError({
                    'identificacion_padre': self.error_messages['required'],
                    'identificacion_madre': self.error_messages['required'],
                })
        return data

    def get_graph_id(self, obj):
        return obj.id

    def get_edit_link(self, obj):
        request = self.context.get('request', None)

        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None
        
        return obj.detail_url(request.user)

    def get_historias_link(self, obj):
        request = self.context.get('request', None)

        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None
        if request and not request.user.has_perm('historias.puede_ver_historias'):
            return None

        return reverse('pacientes:historias', kwargs={'pk': obj.pk})

    def get_citas_url(self, obj):
        request = self.context.get('request', None)
        return obj.citas_url(request.user)

    def get_pagos_url(self, obj):
        request = self.context.get('request', None)
        return obj.pagos_url(request.user)

    def get_tratamientos_url(self, obj):
        request = self.context.get('request', None)
        return obj.tratamientos_url(request.user)


class AcompananteOrdenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Acompanante."""

    class Meta:
        model = models.Acompanante
        fields = ['id', 'nombre', 'telefono', 'direccion', 'parentesco']


class OrdenInfoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Orden. Solo guarda los datos basicos de la orden."""

    acompanante = AcompananteOrdenSerializer(required=False)

    class Meta:
        model = models.Orden
        fields = [
            'id', 'plan', 'institucion', 'afiliacion', 'tipo_usuario', 'asistio_acompanante',
            'acompanante', 'medico_ordena'
        ]
        extra_kwargs = {
            'afiliacion': {'required': True},
            'institucion': {'required': True},
            'tipo_usuario': {'required': True},
        }
    
    def validate(self, data):
        """Valida que si asistio_acompanante es True, los datos del acompanante son requeridos."""

        if data.get('asistio_acompanante', False) and not data.get('acompanante', None):
            raise serializers.ValidationError({'acompante': {
                'nombre': self.error_messages['required'],
                'telefono': self.error_messages['required'],
                'direccion': self.error_messages['required'],
                'parentesco': self.error_messages['required'],
            }}, code='required')

        return data
    
    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance


class AgregarServicioOrdenSerializer(serializers.ModelSerializer):

    fecha = serializers.DateTimeField()
    duracion = serializers.DurationField()
    autorizacion = serializers.CharField(required=False)
    fecha_autorizacion = serializers.DateField(required=False)
    sucursal = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all())
    medico = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.medicos())

    class Meta:
        model = models.ServicioRealizar
        fields = [
            'servicio', 'cantidad', 'coopago', 'sucursal', 'medico', 'fecha', 'duracion',
            'autorizacion', 'fecha_autorizacion', 'orden', 'is_coopago_total', 'is_una_cita'
        ]
        extra_kwargs = {
            'cantidad': {'required': True},
            'coopago': {'required': True},
        }
    
    def create(self, validated_data):
        empleado = self.context['request'].user.empleado
        return models.ServicioRealizar.objects.agregar_a_orden(empleado=empleado, **validated_data)


class TratamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id', 'servicio', 'cantidad', 'coopago', 'valor', 'is_coopago_total', 'is_una_cita', 'num_sesiones_coopago']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.update(empleado=empleado, **validated_data)
        return instance


class RecibirTratamientoTerminadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.recibido_por = empleado
        instance.recibido_at = timezone.now()
        instance.save()
        return instance


class VerificarTratamientoTerminadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.verificado_por = empleado
        instance.verificado_at = timezone.now()
        instance.save()
        return instance

class VerificarInicioTratamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.verificado_inicio_por = empleado
        instance.verificado_inicio_at = timezone.now()
        instance.save()
        return instance

class VerificarInicioAdminTratamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.verificado_inicio_admin_por = empleado
        instance.verificado_inicio_admin_at = timezone.now()
        instance.save()
        return instance

class ReagendarCitasSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicioRealizar
        fields = ['id']
    
    def update(self, instance, validadted_data):
        empleado = self.context['request'].user.empleado
        instance.reagendar_citas(empleado)
        return instance
