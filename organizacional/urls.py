from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^medicos/$', views.ListarMedicosView.as_view(),name='medicos'),
    url(r'^empleados/$', views.ListarEmpleadosView.as_view(),name='empleados'),
    url(r'^sucursales/$', views.ListarSucursalesView.as_view(), name='listar-sucursales'),
    url(r'^horario-atencion/$', views.HorarioAtencionView.as_view(),name='horario-atencion'),
    url(r'^instituciones/$', views.ListarInstitucionesView.as_view(), name='listar-instituciones'),
]
