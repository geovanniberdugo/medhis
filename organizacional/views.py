from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView


class HorarioAtencionView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Ingresa el horario de atención de un medico."""

    template_name = 'organizacional/horario_atencion.html'
    permission_required = 'organizacional.can_add_horario_atencion'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class ListarSucursalesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'organizacional/sucursales.html'
    permission_required = 'organizacional.add_sucursal'

class ListarInstitucionesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'organizacional/instituciones.html'
    permission_required = 'organizacional.add_institucion'

class ListarEmpleadosView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'organizacional/empleados.html'
    permission_required = 'organizacional.add_empleado'

class ListarMedicosView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'organizacional/medicos.html'
    permission_required = 'organizacional.can_add_empleado'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)


