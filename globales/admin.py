from django.contrib import admin
from import_export.admin import ImportExportMixin
from . import models

@admin.register(models.Departamento)
class DepartamentoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

@admin.register(models.Profesion)
class DepartamentoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

@admin.register(models.Municipio)
class DepartamentoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

@admin.register(models.Poblado)
class DepartamentoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

@admin.register(models.Cie)
class DepartamentoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

