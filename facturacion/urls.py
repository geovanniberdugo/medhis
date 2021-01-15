from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.FacturarClienteView.as_view(), name='facturar-cliente'),
    url(r'^cajas/$', views.CajasView.as_view(), name='cajas'),
    url(r'^rips/$', views.GenerarRipsView.as_view(), name='rips'),
    url(r'^siigo/$', views.FacturacionSiigoView.as_view(), name='siigo'),
    url(r'^(?P<pk>\d+)/$', views.DetalleFacturaView.as_view(), name='detalle'),
    url(r'^(?P<pk>\d+)/recibo/$', views.PrintReciboView.as_view(), name='recibo'),    
    url(r'^cajas/(?P<pk>\d+)/$', views.DetalleCajaView.as_view(), name='detalle-caja'),
    url(r'^contabilidad/recibos-caja$', views.ContabilizacionRecibosCajaView.as_view(), name='contabilidad-recibos-caja'),
]
