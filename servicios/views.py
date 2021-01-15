from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from rest_framework import generics
from .serializers import ClienteSerializer, PlanSerializer, TarifaClienteSerializer
from .models import Cliente, Plan, Tarifa


class ListarTarifasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'servicios/tarifas.html'
    permission_required = 'servicios.can_add_tarifa'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class ListarServiciosView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'servicios/servicios.html'
    permission_required = 'servicios.add_servicio'

class ListarClientesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'servicios/clientes.html'
    permission_required = 'servicios.add_cliente'

class ListarPlanesView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'servicios/planes.html'
    permission_required = 'servicios.add_plan'
    queryset = Cliente.objects.all()

# --------------------------
class ListarEmpresasView(generics.ListAPIView):
    """Permite listar empresas."""

    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()

class ServiciosEmpresaView(generics.ListAPIView):
    """Permite listar los servicios de una empresa."""

    serializer_class = TarifaClienteSerializer

    def get_queryset(self):
        return Tarifa.objects.select_related('servicio').filter(plan=self.plan)
    
    def get(self, request, *args, **kwargs):
        self.plan = get_object_or_404(Plan, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)
