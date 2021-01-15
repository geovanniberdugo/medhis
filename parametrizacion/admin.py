from reversion.admin import VersionAdmin
from django.contrib import admin
from common.utils import prettified_json_data
from . import models

@admin.register(models.Rips)
class RipsAdmin(VersionAdmin):
    save_on_top = True
    readonly_fields = ['data_prettified']

    def data_prettified(self, instance):
        """Muestra los datos mas legibles."""

        return prettified_json_data(instance.data)

    data_prettified.short_description = 'data prettified'

@admin.register(models.Configuracion)
class ConfiguracionAdmin(VersionAdmin):
    pass