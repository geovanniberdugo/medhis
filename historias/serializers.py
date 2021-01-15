from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_flex_fields import FlexFieldsModelSerializer
from . import models


class FormatoSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Formato."""

    class Meta:
        model = models.Formato
        fields = ['id', 'nombre', 'contenido', 'valores_por_defecto']


class HistoriaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Historia."""

    nombre_servicio = serializers.SerializerMethodField()
    url_adjunto = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()
    paciente_graph_id = serializers.SerializerMethodField()
    paciente_id = serializers.SerializerMethodField()
    sesion_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Historia
        fields = [
            'id', 'nombre_servicio', 'terminada', 'data', 'formato', 'cita',
            'url_adjunto', 'is_editable', 'paciente_id',
            'paciente_graph_id', 'sesion_id'
        ]
    
    def create(self, validated_data):
        empleado = self.context['request'].user.empleado
        return models.Historia.objects.create_encounter(proveedor=empleado, **validated_data)
    
    def get_nombre_servicio(self, obj):
        return obj.sesion.servicio.servicio.nombre

    def get_url_adjunto(self, obj):
        return reverse('historias:adjuntos', args=(obj.sesion_id, ))

    def get_is_editable(self, obj):
        if 'request' in self.context and obj.terminada:
            return self.context['request'].user.has_perm('historias.puede_editar_historias')
        return not obj.terminada

    def get_paciente_graph_id(self, obj):
        return obj.sesion.servicio.orden.paciente_id

    def get_paciente_id(self, obj):
        return obj.sesion.servicio.orden.paciente_id

    def get_sesion_id(self, obj):
        return obj.cita_id


class AdjuntoSerializer(FlexFieldsModelSerializer):
    """"Serializer para el modelo Adjunto."""

    nombre = serializers.SerializerMethodField()
    url_delete = serializers.SerializerMethodField()
    encounter_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Adjunto
        fields = ['id', 'archivo', 'nombre', 'url_delete', 'encounter_url']
    
    def get_nombre(self, obj):
        split_name = obj.archivo.name.split('/')
        return split_name[-1]

    def get_url_delete(self, obj):
        return reverse('historias:adjuntos-eliminar', args=(obj.id, ))
    
    def get_encounter_url(self, obj):
        return obj.encounter_url()
