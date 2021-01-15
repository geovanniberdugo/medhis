from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, DetailView

class CrearSatisfaccionGlobalView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'encuestas/satisfaccion_global.html'
    permission_required = 'encuestas.puede_crear_encuesta'
