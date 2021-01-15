from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from facturacion.models import ReciboCaja
from agenda.models import Cita
from . import resources
from . import models

class AcompananteInline(admin.StackedInline):
    model = models.Acompanante

class ServicioRealizarInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = models.ServicioRealizar

class CitaInline(admin.StackedInline):
    extra = 0
    model = Cita
    show_change_link = True
    raw_id_fields = ['detalle_factura', 'medico', 'sucursal']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('servicio_prestado__orden__paciente', 'medico', 'sucursal', 'detalle_factura')

class ReciboCajaInline(admin.TabularInline):
    extra = 0
    model = ReciboCaja
    show_change_link=True
    raw_id_fields = ['empleado', 'sucursal', 'anulado_por']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('empleado', 'sucursal')

@admin.register(models.Orden)
class OrdenAdmin(VersionAdmin):
    save_on_top = True
    list_filter = ['institucion']
    raw_id_fields = ['paciente', 'plan']
    inlines = [AcompananteInline, ServicioRealizarInline]
    list_display = ['id', 'paciente', 'plan', 'institucion']
    list_select_related = ['paciente', 'plan', 'institucion']
    search_fields = [
        'id', 'paciente__primer_nombre', 'paciente__segundo_nombre',
        'paciente__primer_apellido', 'paciente__segundo_apellido'
    ]

@admin.register(models.ServicioRealizar)
class ServicioRealizarAdmin(VersionAdmin):
    save_on_top = True
    raw_id_fields = ['orden']
    inlines = [CitaInline, ReciboCajaInline]
    search_fields = ['servicio__nombre', 'orden__id', 'id']
    list_filter = ['estado', 'is_coopago_total', 'is_una_cita']
    list_display = ['id', 'cantidad', 'servicio', 'coopago', 'estado', 'orden', 'convenio']
    list_select_related = ['servicio', 'orden', 'orden__paciente', 'orden__plan', 'orden__plan__cliente']


@admin.register(models.Paciente)
class PacienteAdmin(ImportExportMixin, VersionAdmin):
    save_on_top = True
    readonly_fields = ['creado_el']
    resource_class = resources.PacienteResource
    list_display = ['__str__', 'numero_documento', 'fecha_ingreso']
    search_fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_documento']
