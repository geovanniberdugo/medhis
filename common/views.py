import csv
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django_extras.views import ExtraGraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from agenda.schema import loaders as agenda_loaders
from pacientes.schema import loaders as paciente_loaders
from servicios.schema import loaders as servicios_loaders
from facturacion.schema import loaders as facturacion_loaders
from historias.schema import loaders as historia_loaders

class GQLContext:
    # Ordenes
    @cached_property
    def plan_by_orden(self):
        return paciente_loaders.PlanByOrden()

    @cached_property
    def institucion_by_orden(self):
        return paciente_loaders.institucionByOrden()

    # Tratamientos
    @cached_property
    def coopago_bruto_by_tratamiento(self):
        return paciente_loaders.CoopagoBrutoByTratamiento()

    @cached_property
    def iva_coopago_by_tratamiento(self):
        return paciente_loaders.IvaCoopagoByTratamiento()

    @cached_property
    def orden_by_tratamiento(self):
        return paciente_loaders.OrdenByTratamiento()

    @cached_property
    def medicos_by_tratamiento(self):
        return paciente_loaders.MedicosByTratamiento()

    @cached_property
    def facturas_by_tratamiento(self):
        return paciente_loaders.FacturasByTratamiento()
    
    @cached_property
    def servicio_by_tratamiento(self):
        return paciente_loaders.ServicioByTratamiento()

    @cached_property
    def paciente_by_tratamiento(self):
        return paciente_loaders.PacienteByTratamiento()

    @cached_property
    def convenio_by_tratamiento(self):
        return paciente_loaders.ConvenioByTratamiento()

    @cached_property
    def entidad_by_tratamiento(self):
        return paciente_loaders.EntidadByTratamiento()

    @cached_property
    def fecha_inicio_by_tratamiento(self):
        return paciente_loaders.FechaInicioByTratamiento()

    @cached_property
    def total_pagado_by_tratamiento(self):
        return paciente_loaders.TotalPagadoByTratamiento()

    @cached_property
    def saldo_paciente_by_tratamiento(self):
        return paciente_loaders.SaldoPacienteByTratamiento()

    @cached_property
    def saldo_sesiones_by_tratamiento(self):
        return paciente_loaders.SaldoSesionesByTratamiento()

    @cached_property
    def cant_citas_atendidas_by_tratamiento(self):
        return paciente_loaders.CantCitasAtendidasByTratamiento()

    @cached_property
    def valor_pagar_medico_by_tratamiento(self):
        return paciente_loaders.ValorPagarMedicoByTratamiento()

    @cached_property
    def cant_citas_faltantes_by_tratamiento(self):
        return paciente_loaders.CantCitasFaltantesByTratamiento()

    # Recibos de caja
    @cached_property
    def sucursal_by_recibo_caja(self):
        return facturacion_loaders.SucusalByReciboCaja()

    @cached_property
    def paciente_by_recibo_caja(self):
        return facturacion_loaders.PacienteByReciboCaja()

    # Facturas
    @cached_property
    def total_by_factura(self):
        return facturacion_loaders.TotalByFactura()

    # Planes
    @cached_property
    def nombre_completo_by_plan(self):
        return servicios_loaders.NombreCompletoByPlan()

    @cached_property
    def cliente_by_plan(self):
        return servicios_loaders.ClienteByPlan()
    
    # Servicios
    @cached_property
    def tarifas_by_servicio(self):
        return servicios_loaders.TarifasByServicio()

    # Citas
    @cached_property
    def convenio_by_cita(self):
        return agenda_loaders.ConvenioByCita()

    @cached_property
    def estado_display_by_cita(self):
        return agenda_loaders.EstadoDisplayByCita()

    @cached_property
    def medico_by_cita(self):
        return agenda_loaders.MedicoByCita()

    @cached_property
    def tratamiento_by_cita(self):
        return agenda_loaders.TratamientoByCita()

    @cached_property
    def sucursal_by_cita(self):
        return agenda_loaders.SucursalByCita()

    @cached_property
    def servicio_by_cita(self):
        return agenda_loaders.ServicioByCita()

    @cached_property
    def can_move_by_cita(self):
        return agenda_loaders.CanMoveByCita()

    @cached_property
    def paciente_by_cita(self):
        return agenda_loaders.PacienteByCita()

    @cached_property
    def historial_actual_by_cita(self):
        return agenda_loaders.HistorialActualByCita()
    
    @cached_property
    def can_add_encuentro_by_cita(self):
        return agenda_loaders.CanAddEncuentroByCita()

    @cached_property
    def cumplida_by_cita(self):
        return agenda_loaders.CumplidaByCita()

    @cached_property
    def terminada_by_cita(self):
        return agenda_loaders.TerminadaByCita()

    @cached_property
    def cancelada_by_cita(self):
        return agenda_loaders.CanceladaByCita()

    @cached_property
    def estados_disponibles_by_cita(self):
        return agenda_loaders.EstadosDisponiblesByCita()

    @cached_property
    def detalle_factura_by_cita(self):
        return agenda_loaders.DetalleFacturaByCita()

    @cached_property
    def encuentros_by_cita(self):
        return agenda_loaders.EncuentrosByCita()
    
    # Historia
    @cached_property
    def proveedor_by_historia(self):
        return historia_loaders.ProveedorByHistoria()

    @cached_property
    def formato_by_historia(self):
        return historia_loaders.FormatoByHistoria()

    @cached_property
    def print_content_by_historia(self):
        return historia_loaders.PrintContentByHistoria()

class CustomGraphQLView(LoginRequiredMixin, FileUploadGraphQLView, ExtraGraphQLView):
    
    def get_context(self, request):
        request.dataloaders = GQLContext()
        return request

class FileResponseMixin:
    def csv_response(self, data, name, delimiter='|'):
        """
        :param data: Lista con los datos a convertir en csv.
        :param name: Nombre del archivo.
        :param delimiter: Separador de datos.
        """

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)

        writer = csv.writer(response, delimiter=delimiter)
        writer.writerows(data)
        return response
    
    def txt_response(self, data, name):
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)
        return response

class HomeView(LoginRequiredMixin, TemplateView):
    """Dashboard."""

    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

