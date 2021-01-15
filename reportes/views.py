from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import OportunidadCitaForm, CitasServicioEntidadForm, IndMortalidadMorbilidadForm, CertificadoAsistenciaForm


class TratamientosNoFacturadosEntidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/tratamientos_no_facturados_entidad.html'
    permission_required = 'reportes.can_see_tratamientos_no_facturados_entidad'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class ReporteMedicosOrdenanTratamientoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/medicos_ordenan_tratamiento.html'
    permission_required = 'reportes.can_see_medicos_ordenan_tratamiento'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class ReporteAsignacionCitasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/asignacion_citas.html'
    permission_required = 'reportes.can_see_asignacion_citas'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class ReporteCitasNoCumplidasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/citas_no_cumplidas.html'
    permission_required = 'reportes.can_see_citas_no_cumplidas'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class TratamientosPagoTerapeutasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/tratamientos_pago_terapeutas.html'
    permission_required = 'reportes.can_see_tratamientos_pago_profesional'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class TratamientosPagoMedicosView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/tratamientos_pago_medicos.html'
    permission_required = 'reportes.can_see_tratamientos_pago_profesional'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class CertificadoAsistenciaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/certificado_asistencia.html'
    permission_required = 'reportes.can_see_certificado_asistencia'

    def get(self, request, *args, **kwargs):
        self.empleado = getattr(request.user, 'empleado', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        institucion, paciente, citas, sucursales, entidad = self.report_data(self.request.GET)

        kwargs.update({
            'citas': citas,
            'polymer3': True,
            'entidad': entidad,
            'paciente': paciente,
            'sucursales': sucursales,
            'empleado': self.empleado,
            'institucion': institucion,
        })
        return super().get_context_data(**kwargs)
    
    def report_data(self, data):
        form = CertificadoAsistenciaForm(data)

        if form.is_valid():
            return form.report_data()

        return (None, None, [])

class TratamientosFacturadosEntidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/tratamientos_facturados_entidad.html'
    permission_required = 'reportes.can_see_tratamientos_facturado_entidad'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class RelacionFacturasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = 'reportes/relacion_facturas.html'
    permission_required = 'reportes.can_see_relacion_facturas'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class RelacionRecibosCajaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Relacion de recibos de caja."""

    template_name = 'reportes/relacion_recibos_caja.html'
    permission_required = 'reportes.can_see_relacion_recibos_caja'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class RelacionCitasPacienteView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Muestra la relacion de citas agrupadas por IPS de un paciente
    especifico en un rango de fechas.
    """

    template_name = 'reportes/relacion_citas_paciente.html'
    permission_required = 'reportes.can_see_citas_paciente'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class RelacionCitasProfesionalView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Muestra la relacion de citas agrupadas por servicio de un profesional
    especifico en un rango de fechas.
    """

    template_name = 'reportes/relacion_tratamientos_terminados_medico.html'
    permission_required = 'reportes.can_see_tratamientos_terminado_profesional'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class TratamientosNoTerminadosProfesionalView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Muestra los tratamientos no terminados de un profesional segun su fecha de inicio."""

    template_name = 'reportes/tratamientos_no_terminados_profesional.html'
    permission_required = 'reportes.can_see_tratamientos_no_terminado_profesional'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class TratamientosIniciadosProfesionalView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Muestra los tratamientos de un profesional que iniciaron en un rango de fechas."""

    template_name = 'reportes/profesional_tratamientos_iniciados.html'
    permission_required = 'reportes.can_see_tratamientos_iniciados_profesional'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class OportunidadCitaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Indicador de oportunidad de cita."""

    template_name = 'reportes/oportunidad_cita.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class PrintOportunidadCitaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Reporte para imprimir oportunidad de cita."""

    template_name = 'reportes/oportunidad_cita_print.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def report_data(self, data):
        form = OportunidadCitaForm(data)
        if form.is_valid():
            return form.report_data()

        return (None, None, None, {})

    def get_context_data(self, **kwargs):
        desde, hasta, institucion, data = self.report_data(self.request.GET)

        kwargs.update({
            'data': data,
            'desde': desde,
            'hasta': hasta,
            'polymer3': True,
            'institucion': institucion,
        })
        return super().get_context_data(**kwargs)

class TotalCitasServicioEntidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Total de citas por servicio y entidad."""

    template_name = 'reportes/citas_servicio_entidad.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class PrintTotalCitasServicioEntidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Reporte para imprimir el total de citas por servicio y entidad."""

    template_name = 'reportes/citas_servicio_entidad_print.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def report_data(self, data):
        form = CitasServicioEntidadForm(data)
        if form.is_valid():
            return form.report_data()

        return (None, None, None, {})

    def get_context_data(self, **kwargs):
        desde, hasta, institucion, data = self.report_data(self.request.GET)

        kwargs.update({
            'data': data,
            'desde': desde,
            'hasta': hasta,
            'polymer3': True,
            'institucion': institucion,
        })
        return super().get_context_data(**kwargs)

class IndMortalidadMorbilidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Indicadores de mortalidad, morbilidad y eventos adversos."""

    template_name = 'reportes/ind_mortalidad_morbilidad.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class PrintIndMortalidadMorbilidadView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Reporte para imprimir los indicadores de mortalidad, morbilidad y eventos adversos."""

    template_name = 'reportes/ind_mortalidad_morbilidad_print.html'
    permission_required = 'agenda.can_generar_indicadores_resolucion_256'

    def report_data(self, data):
        form = IndMortalidadMorbilidadForm(data)
        if form.is_valid():
            return form.report_data()

        return (None, None, None, {})

    def get_context_data(self, **kwargs):
        desde, hasta, institucion, data = self.report_data(self.request.GET)

        kwargs.update({
            'data': data,
            'desde': desde,
            'hasta': hasta,
            'polymer3': True,
            'institucion': institucion,
        })
        return super().get_context_data(**kwargs)
