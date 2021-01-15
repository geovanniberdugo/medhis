from django.contrib import admin
from import_export import resources
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from . import models

class PlanResource(resources.ModelResource):

    class Meta:
        model = models.Plan
        exclude = ['servicios']

class TarifaResource(resources.ModelResource):

    class Meta:
        model = models.Tarifa
        import_id_fields = ['plan', 'institucion', 'servicio']

class PlanInline(admin.TabularInline):
    extra = 0
    model = models.Plan
    show_change_link = True

@admin.register(models.Cliente)
class ClienteAdmin(ImportExportMixin, VersionAdmin):
    inlines = [PlanInline]
    search_fields = ['nombre']
    list_display = ['nombre', 'sesiones_autorizacion', 'discriminar_iva', 'factura_paciente']

class TarifaInline(admin.TabularInline):
    extra = 0
    model = models.Tarifa
    show_change_link = True

@admin.register(models.Plan)
class PlanAdmin(ImportExportMixin, VersionAdmin):
    inlines = [TarifaInline]
    resource_class = PlanResource
    list_select_related = ['cliente']
    list_display = ['nombre', 'cliente']
    search_fields = ['nombre', 'cliente__nombre']

@admin.register(models.Servicio)
class ServicioAdmin(ImportExportMixin, VersionAdmin):
    list_filter = ['tipo']
    search_fields = ['nombre']
    list_select_related = ['tipo']
    list_display = ['nombre', 'cups', 'tipo']

@admin.register(models.Tipo)
class TipoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ['nombre', 'clase', 'in_indicadores']

@admin.register(models.Tarifa)
class TarifaAdmin(ImportExportMixin, VersionAdmin):
    resource_class = TarifaResource
    list_select_related = ['plan', 'servicio']
    list_display = ['plan', 'servicio', 'institucion', 'valor', 'coopago']

