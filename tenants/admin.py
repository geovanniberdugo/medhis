from django.contrib import admin
from . import models

@admin.register(models.Tenant)
class TenantAdmin(admin.ModelAdmin):
    pass


