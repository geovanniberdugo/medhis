from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.SatisfaccionGlobal)
class SatisfaccionGlobalAdmin(VersionAdmin):
    list_display = ['fecha', 'pregunta1', 'pregunta2']

@admin.register(models.EventoAdverso)
class EventoAdversoAdmin(VersionAdmin):
    list_display = ['fecha', 'caida', 'tipo_caida', 'medicamentos']
