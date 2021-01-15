from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.ReciboCaja)
class ReciboCajaAdmin(VersionAdmin):
    save_on_top = True
    readonly_fields = ['fecha']
    raw_id_fields = ['servicio_prestado']
    search_fields = ['id', 'numero', 'servicio_prestado__id', 'servicio_prestado__orden__id']
    list_select_related = ['empleado', 'servicio_prestado__servicio', 'servicio_prestado__orden', 'anulado_por', 'sucursal']
    list_display = ['id', 'numero', 'valor', 'fecha', 'sucursal', 'empleado', 'servicio_prestado', 'anulado_por', 'anulado_el']

class DetalleCajaInline(admin.TabularInline):
    extra = 0
    model = models.DetalleCaja

@admin.register(models.Caja)
class CajaAdmin(VersionAdmin):
    inlines = [DetalleCajaInline]
    list_filter = ['empleado', 'fecha']
    list_select_related = ['empleado', 'recibido_por']
    list_display = ['id', 'empleado', 'fecha', 'total', 'recibido_por', 'recibido_at']

class DetalleFacturaInline(admin.TabularInline):
    extra = 0
    readonly_fields = ['citas']
    model = models.DetalleFactura

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('citas')

    def citas(self, obj):
        return ' - '.join(map(lambda o: str(o.id), obj.citas.all()))
    citas.short_description = 'citas'

@admin.register(models.Factura)
class FacturaAdmin(VersionAdmin):
    inlines = [DetalleFacturaInline]
    search_fields = ['id', 'numero']
    list_select_related = ['anulado_por']
    list_filter = ['institucion', 'cliente']
    list_display = ['id', 'numero', 'fecha_expedicion', 'institucion', 'cliente', 'anulado_por']

@admin.register(models.ParametroFacturaSiigo)
class ParametroFacturaSiigoAdmin(VersionAdmin):
    list_select_related = ['tipo_servicio']
    list_display = ['id', 'tipo_servicio', 'tipo_cliente', 'cuenta_puc', 'codigo_linea', 'codigo_producto']
