from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from common.utils import prettified_json_data
from agenda.models import Cita
from .  import models


class AdjuntoInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = models.Adjunto

@admin.register(models.Historia)
class HistoriaAdmin(VersionAdmin):
    save_on_top = True
    raw_id_fields = ['cita']
    inlines = [AdjuntoInline]
    readonly_fields = ['data_prettified', 'fecha']
    list_display = ['id', 'cita', 'fecha', 'proveedor', 'terminada']
    list_select_related = ['proveedor', 'cita__servicio_prestado__orden__paciente']
    search_fields = ['=id', 'proveedor__nombres', 'proveedor__apellidos', '=cita__servicio_prestado__id']

    def data_prettified(self, instance):
        """Muestra los datos de la historia mas legibles."""

        return prettified_json_data(instance.data)

    data_prettified.short_description = 'data prettified'


@admin.register(models.Formato)
class FormatoAdmin(ImportExportMixin, VersionAdmin):
    save_on_top = True
    list_display = ['nombre', 'permiso', 'diagnostico', 'activo']
    readonly_fields = ['contenido_prettified', 'valores_por_defecto_prettified']

    def contenido_prettified(self, instance):
        """Muestra el contenido del formato de una historia mas legible."""

        return prettified_json_data(instance.contenido)

    def valores_por_defecto_prettified(self, instance):
        """Muestra los valores por defecto del formato de una historia mas legible."""

        return prettified_json_data(instance.valores_por_defecto)

    contenido_prettified.short_description = 'contenido prettified'
    valores_por_defecto_prettified.short_description = 'valores por defecto prettified'


@admin.register(models.Adjunto)
class AdjuntoAdmin(VersionAdmin):
    pass
