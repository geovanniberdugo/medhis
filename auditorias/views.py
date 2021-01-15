from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PacientsTerminaronTratamiento(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Permite verificar y auditar si la cantidad de firmas registradas en la orden coincide con el numero
    citas atendidas para los pacientes que terminaron tratamiento.
    """

    template_name = 'auditorias/pacientes_terminaron_tratamiento.html'

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = [
            'pacientes.can_recibir_pacientes_terminaron_tratamiento',
            'pacientes.can_verificar_pacientes_terminaron_tratamiento'
        ]
        return any([self.request.user.has_perm(perm) for perm in perms])
    
    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)
