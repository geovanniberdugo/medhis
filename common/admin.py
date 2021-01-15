from django.contrib import admin
from import_export import resources
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin

User = get_user_model()
admin.site.unregister(User)

class UserResource(resources.ModelResource):
    
    class Meta:
        model = User
        fields = ['id', 'username']

    def after_save_instance(instance, using_transactions, dry_run):
        pass

@admin.register(User)
class UsuarioAdmin(ImportExportMixin, UserAdmin):
    resource_class = UserResource
