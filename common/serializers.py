from rest_framework import serializers, relations


class SelectableSerializerMixin(serializers.Serializer):
    """Mixin que le agrega campos label y value para ser usado en vaadin-combobox."""

    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    mixin_fields = ['label', 'value']

    def get_label(self, obj):
        return str(obj)
    
    def get_value(self, obj):
        return obj.pk

