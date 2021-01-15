from django.db import transaction
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse
from organizacional.models import Institucion
from pacientes.models import Paciente, Orden
from servicios.models import Servicio, Plan
from . import services
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para la creación/actualización del paciente al momento de agendar una cita."""

    class Meta:
        model = Paciente
        fields = [
            'id', 'tipo_documento', 'numero_documento', 'primer_nombre', 'segundo_nombre', 'genero', 'telefono2',
            'primer_apellido', 'segundo_apellido', 'telefono', 'celular', 'direccion', 'fecha_nacimiento'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero_documento'].validators = []

class AgendarCitaSerializar(serializers.ModelSerializer):
    """Serializer para el agendamiento de una cita."""

    paciente = PacienteSerializer()
    duracion = serializers.DurationField()
    institucion = serializers.PrimaryKeyRelatedField(queryset=Institucion.objects.all())
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    convenio = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    estado = serializers.ChoiceField(write_only=True, choices=[
        models.HistorialEstado.NO_CONFIRMADA, models.HistorialEstado.CONFIRMADA, models.HistorialEstado.CUMPLIDA
    ])

    class Meta:
        model = models.Cita
        fields = [
            'id', 'institucion', 'servicio', 'convenio', 'fecha_deseada',
            'paciente', 'estado', 'inicio', 'medico', 'sucursal', 'duracion'
        ]

    def validate(self, data):
        """Valida que el telefono y celular no esten vacios debe ingresar alguno de los dos."""

        if 'paciente' in data and not data['paciente'].get('telefono', None) and not data['paciente'].get('celular', None):
            raise serializers.ValidationError('Debes ingresar el telefono o el celular', code='required')

        return data
    
    @transaction.atomic
    def create(self, validated_data):
        estado = validated_data.pop('estado')
        paciente_data = validated_data.pop('paciente')
        empleado = self.context['request'].user.empleado
        cita = services.agendar_cita(paciente_data, estado, empleado, **validated_data)
        return cita

class MoverCitaSerializer(serializers.ModelSerializer):
    """Serializer para cambiar el horario de una cita."""

    class Meta:
        model = models.Cita
        fields = ['id', 'inicio', 'medico', 'sucursal']
    
    def validate(self, data):
        """Valida que la cita se pueda reprogramar."""

        if not self.instance.can_move:
            raise serializers.ValidationError('La cita no se puede reprogramar porque ya fue atendida.')
        return data
    
    def update(self, instance, validated_data):
        return instance.mover_cita(**validated_data)

class AddAutorizacionCitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cita
        fields = ['id', 'autorizacion', 'fecha_autorizacion', 'autorizado_por']
    
    def update(self, instance, validated_data):
        services.agregar_autorizacion(instance, **validated_data)
        instance.refresh_from_db()
        return instance

class ActualizarEstadoCitaSerializer(serializers.ModelSerializer):

    reagendar = serializers.BooleanField()
    motivo = serializers.CharField(required=False)
    estado = serializers.ChoiceField(choices=models.HistorialEstado.ESTADOS)

    class Meta:
        model = models.Cita
        fields = ['id', 'estado', 'motivo', 'reagendar']
    
    def update(self, instance, validated_data):
        empleado = self.context['request'].user.empleado
        instance.actualizar_estado(empleado=empleado, **validated_data)
        return instance

class TipoAgendaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo tipo de agenda."""

    class Meta:
        model = models.Agenda
        fields = ['id', 'nombre', 'duracion']

class CambiarMotivoEstadoCita(serializers.ModelSerializer):

    class Meta:
        model = models.HistorialEstado
        fields = ['id', 'motivo']