from django.http import Http404
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from common.views import FileResponseMixin
from pacientes.models import Paciente
from .forms import IndicadoresResolucion256Form, AgendaDiariaForm
from .models import Cita, Agenda


class IndicadoresResolucion256View(LoginRequiredMixin, PermissionRequiredMixin, FileResponseMixin, FormView):
    """Indicadores resolucion 256 de 2016."""

    form_class = IndicadoresResolucion256Form
    template_name = 'agenda/indicadores_resolucion_256.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        return self.csv_response(form.generar_datos(), form.nombre_archivo())


class ListarTiposAgendaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'agenda/tipos_agenda.html'
    permission_required = 'agenda.add_agenda'


class AgendaDiariaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Permite listar la agenda diaria de los medicos."""

    template_name = 'agenda/agenda_diaria.html'
    permission_required = 'agenda.can_see_agenda_diaria'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class PrintAgendaDiariaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Permite imprimir la agenda diaria."""

    template_name = 'agenda/print_agenda_diaria.html'
    permission_required = 'agenda.can_see_todas_citas'

    def get_data(self):
        form = AgendaDiariaForm(self.request.GET)
        if form.is_valid():
            citas = form.citas_dia()
            fecha, medico, sucursal = form.get_data()
            return (fecha, medico, sucursal, citas)
        
        return (None, None, None, [])

    def get_context_data(self, **kwargs):
        fecha, medico, sucursal, citas = self.get_data()

        kwargs.update({
            'fecha': fecha,
            'citas': citas,
            'medico': medico,
            'polymer3': True,
            'sucursal': sucursal,
        })
        return super().get_context_data(**kwargs)

class AgendaCitasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Permite agendar citas."""

    template_name = 'agenda/agenda_citas.html'
    permission_required = 'agenda.can_agendar_citas'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)
