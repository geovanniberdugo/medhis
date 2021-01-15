from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from reversion.admin import VersionAdmin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportMixin
from . import models

User = get_user_model()

class EmpleadoResource(resources.ModelResource):

    username = Field(attribute='username')

    class Meta:
        model = models.Empleado
        exclude = ['usuario', 'firma']
    
    def dehydrate_username(self, empleado):
        return empleado.usuario.username if empleado.usuario_id else empleado.username
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if not dry_run and not instance.usuario_id:
            user = User.objects.create_user(instance.username, password=instance.cedula)
            instance.usuario = user
    
    def save_instance(self, instance, using_transactions=True, dry_run=False):
        transaction = False if dry_run else using_transactions
        super().save_instance(instance, using_transactions=transaction, dry_run=dry_run)


@admin.register(models.Institucion)
class InstitucionAdmin(ImportExportMixin, VersionAdmin):
    pass


class HorarioAtencionInline(admin.TabularInline):
    extra = 0
    model = models.HorarioAtencion

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('medico')


@admin.register(models.Empleado)
class EmpleadoAdmin(ImportExportMixin, VersionAdmin):
    resource_class = EmpleadoResource
    inlines = [HorarioAtencionInline]
    list_select_related = ['usuario']
    list_display = [
        'nombres', 'apellidos', 'duracion_cita', 'agenda', 'usuario', 'tipo'
    ]


@admin.register(models.Sucursal)
class SucursalAdmin(ImportExportMixin, VersionAdmin):
    pass


