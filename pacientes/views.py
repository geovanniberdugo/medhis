from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _lazy
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters, status

from agenda.models import Cita
from organizacional.models import Sucursal
from historias.serializers import HistoriaSerializer
from historias.models import Historia, Formato
from .models import Paciente, Orden, ServicioRealizar
from .serializers import PacienteSerializer
from . import serializers

class HistoriasPacienteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Paciente
    template_name = 'pacientes/lista_historias.html'
    permission_required = 'historias.can_see_historias'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'polymer3': True,
        })
        return super().get_context_data(**kwargs)

class DetailPacienteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Paciente
    template_name = 'pacientes/detalle_paciente.html'

    def has_permission(self):
        perms = ['pacientes.can_see_paciente', 'pacientes.can_edit_paciente']
        return any([self.request.user.has_perm(perm) for perm in perms])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'polymer3': True,
            'orden_url': self.get_orden_url()
        })
        return super().get_context_data(**kwargs)
    
    def get_orden_url(self):
        cita_id = self.request.GET.get('cita', None)
        if cita_id:
            cita = get_object_or_404(Cita, pk=cita_id)
            return reverse('pacientes:ordenes-detalle', args=[cita.servicio_prestado.orden_id])


class PacienteNuevoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pacientes/nuevo_paciente.html'
    permission_required = 'pacientes.can_add_paciente'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class TratamientosPacienteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    
    model = Paciente
    template_name = 'pacientes/tratamientos.html'
    permission_required = 'pacientes.can_see_orden'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class PagosPacienteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    
    model = Paciente
    template_name = 'pacientes/pagos.html'
    permission_required = 'facturacion.can_see_recibos_caja'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class CitasPacienteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Paciente
    template_name = 'pacientes/citas.html'
    permission_required = 'agenda.puede_ver_todas_citas'

class ControlCitasView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Permite ver el detalle de una factura e imprimirlo."""

    model = ServicioRealizar
    context_object_name = 'tratamiento'
    template_name = 'pacientes/control_citas.html'
    permission_required = 'pacientes.can_see_orden'

    def get(self, request, *args, **kwargs):
        self.empleado = getattr(request.user, 'empleado', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'polymer3': True,
            'empleado': self.empleado,
            'sucursales': Sucursal.objects.all()
        })
        return super().get_context_data(**kwargs)

class DetalleOrdenView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Orden
    template_name = 'pacientes/detalle_orden.html'
    permission_required = 'pacientes.can_see_orden'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class NuevaHistoriaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pacientes/nueva_historia.html'
    permission_required = 'historias.add_historia'

    def get_sesion(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cita, pk=pk)
    
    def get_formato(self):
        pk = self.kwargs.get('formato_pk')
        return get_object_or_404(Formato, pk=pk)
    
    def get_context_data(self, **kwargs):
        sesion = self.get_sesion()
        formato = self.get_formato()
        return super().get_context_data(sesion=sesion, formato=formato, **kwargs)

class HistoriasSesionView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'pacientes/historias_sesion.html'
    permission_required = 'historias.add_historia'
    model = Cita

class PacientesList(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_documento')
    filter_fields = ('numero_documento',)

class ListarPacientesView(generics.ListCreateAPIView):
    """Permite buscar un paciente según sus nombres, apellidos o número de documento y crear pacientes."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/lista_pacientes.html'
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_documento')
    filter_fields = ('numero_documento',)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT', '').lower() == 'application/json':
            return super().get(request, *args, **kwargs)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = PacienteSerializer(queryset, many=True, context={'request': request})
            pacientes = JSONRenderer().render(serializer.data)
            return Response({'pacientes': pacientes})

