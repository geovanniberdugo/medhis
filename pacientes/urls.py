from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ListarPacientesView.as_view(), name='listar'),
    url(r'^nuevo$', views.PacienteNuevoView.as_view(), name='crear'),
    url(r'^(?P<pk>\d+)/$', views.DetailPacienteView.as_view(), name='detalle'),
    url(r'^(?P<pk>\d+)/historias/$', views.HistoriasPacienteView.as_view(), name='historias'),
    
    url(r'^(?P<pk>\d+)/pagos/$',views.PagosPacienteView.as_view(), name='pagos'),
    url(r'^(?P<pk>\d+)/citas/$', views.CitasPacienteView.as_view(), name='citas'),
    url(r'^ordenes/(?P<pk>\d+)/$', views.DetalleOrdenView.as_view(), name='ordenes-detalle'),
    url(r'^control-citas/(?P<pk>\d+)/$', views.ControlCitasView.as_view(), name='control-citas'),
    url(r'^(?P<pk>\d+)/tratamientos/$',views.TratamientosPacienteView.as_view(), name='tratamientos'),
    url(r'^sesiones/(?P<pk>\d+)/historias/$', views.HistoriasSesionView.as_view(), name='historias-sesion'),
    url(r'^sesiones/(?P<pk>\d+)/historias/(?P<formato_pk>\d+)$', views.NuevaHistoriaView.as_view(), name='nueva-historia'),

    url(r'^list/$', views.PacientesList.as_view()),
]
