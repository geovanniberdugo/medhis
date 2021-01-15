from django.contrib import admin
from reversion.admin import VersionAdmin
from pacientes.models import ServicioRealizar
from . import models


class HistorialEstadoInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    readonly_fields = ['fecha']
    model = models.HistorialEstado


@admin.register(models.HistorialEstado)
class HistorialEstadoAdmin(VersionAdmin):
    
    raw_id_fields = ['cita']
    readonly_fields = ['fecha']


@admin.register(models.Cita)
class CitaAdmin(VersionAdmin):
    readonly_fields = ['creada_el']
    inlines = [HistorialEstadoInline]
    list_filter = ['sucursal', 'medico']
    raw_id_fields = ['servicio_prestado']
    list_display = ('id', 'paciente', 'servicio_prestado', 'inicio', 'fin', 'medico', 'sucursal', 'estado_display')
    search_fields = ['=id', '=servicio_prestado__id', '=servicio_prestado__orden__id', 'servicio_prestado__orden__paciente__primer_nombre']
    list_select_related = ['servicio_prestado', 'medico', 'sucursal', 'servicio_prestado__servicio', 'servicio_prestado__orden__paciente']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate_estado()


@admin.register(models.Agenda)
class AgendaAdmin(VersionAdmin):
    pass
