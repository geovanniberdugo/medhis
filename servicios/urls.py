from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ListarServiciosView.as_view(), name='listar'),
    url(r'^tarifas/$', views.ListarTarifasView.as_view(), name='listar-tarifas'),
    url(r'^clientes/$', views.ListarClientesView.as_view(), name='listar-clientes'),
    url(r'^clientes/(?P<pk>\d+)/planes/$', views.ListarPlanesView.as_view(), name='listar-planes'),

    url(r'^empresas/$', views.ListarEmpresasView.as_view(), name='empresas'),
    url(r'^empresas/(?P<pk>\d+)/servicios/$', views.ServiciosEmpresaView.as_view(), name='empresas_servicios'),
]