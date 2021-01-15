import io
import csv
from zipfile import ZipFile
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from common.views import FileResponseMixin
from .forms import RipsForm, ContabilidadForm, ContabilizacionRecibosForm, FacturacionSiigoForm
from .siigo import write_to_excel
from . import models

class FacturacionSiigoView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'facturacion/facturacion_siigo.html'
    permission_required = 'facturacion.can_facturar'
    form_class = FacturacionSiigoForm

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        data = form.exportar_facturas()
        _file = write_to_excel(data) 
        response = HttpResponse(_file, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=facturacion.xlsx'
        return response

class FacturarClienteView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'facturacion/facturar_cliente.html'
    permission_required = 'facturacion.can_facturar'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class DetalleFacturaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Permite ver el detalle de una factura e imprimirlo."""

    model = models.Factura
    permission_required = 'facturacion.can_facturar'
    template_name = 'facturacion/detalle_factura.html'
    queryset = models.Factura.objects.select_related('institucion', 'cliente', 'institucion__firma_factura').all()

    def quien_firma(self):
        return self.object.institucion.firma_factura
    
    def detalle(self):
        return sorted(
            self.object.detalle.prefetch_related('citas__servicio_prestado__servicio', 'citas__servicio_prestado__orden__paciente').all(),
            key=lambda x: (str(x.paciente), x.fecha_atencion)
        )

    def get_context_data(self, **kwargs):
        kwargs.update({
            'polymer3': True,
            'detalle': self.detalle(),
            'quien_firma': self.quien_firma(),
        })
        return super().get_context_data(**kwargs)

class GenerarRipsView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """Generación de RIPS."""

    form_class = RipsForm
    template_name = 'facturacion/generar_rips.html'
    permission_required = 'facturacion.can_facturar'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        mem_file = io.BytesIO()
        data = form.generar_rips()
        with ZipFile(mem_file, 'w') as zip_file:
            for nombre, content in data:
                zip_file.writestr(nombre, content)
        
        mem_file.seek(0)
        response = HttpResponse(mem_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=rips.zip'
        return response

class ContabilizacionRecibosCajaView(LoginRequiredMixin, PermissionRequiredMixin, FileResponseMixin, FormView):
    """Integración con contabilidad (Siigo)"""

    form_class = ContabilizacionRecibosForm
    template_name = 'facturacion/contabilizacion_recibos_caja.html'
    permission_required = 'facturacion.can_contabilizar_recibo_caja'

    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        nombre, data = form.exportar()
        return self.txt_response(data, nombre)

class PrintReciboView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Permite ver el detalle de un Recibo de Caja e imprimirlo."""

    model = models.ReciboCaja
    template_name = 'facturacion/detalle_recibo.html'
    permission_required = 'facturacion.print_recibo'

class CajasView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Lista las cajas."""

    template_name = 'facturacion/cajas.html'

    def has_permission(self):
        perms = ['facturacion.can_see_todas_cajas', 'facturacion.can_cerrar_caja']
        return any(self.request.user.has_perm(perm) for perm in perms)
    
    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)

class DetalleCajaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Permite ver el detalle del cierre de caja e imprimirlo."""

    model = models.Caja
    template_name = 'facturacion/detalle_caja.html'
    
    def has_permission(self):
        perms = ['facturacion.can_see_todas_cajas', 'facturacion.can_cerrar_caja']
        return any(self.request.user.has_perm(perm) for perm in perms)
    
    def get_context_data(self, **kwargs):
        kwargs.update({'polymer3': True})
        return super().get_context_data(**kwargs)
