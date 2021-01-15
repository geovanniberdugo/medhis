from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^relacion-facturas/$',views.RelacionFacturasView.as_view(), name='relacion-facturas'),
    url(r'^oportunidad-citas/$', views.OportunidadCitaView.as_view(), name='oportunidad-citas'),
    url(r'^relacion-recibos-caja/$', views.RelacionRecibosCajaView.as_view(), name='recibos-caja'),
    url(r'^asignacion-citas/$', views.ReporteAsignacionCitasView.as_view(), name='asignacion-citas'),
    url(r'^citas-no-cumplidas/$', views.ReporteCitasNoCumplidasView.as_view(), name='citas-no-cumplidas'),
    url(r'^certificado-asistencia/$', views.CertificadoAsistenciaView.as_view(), name='certificado-asistencia'),
    url(r'^oportunidad-citas-print/$', views.PrintOportunidadCitaView.as_view(), name='oportunidad-citas-print'),
    url(r'^relacion-citas-paciente/$', views.RelacionCitasPacienteView.as_view(), name='relacion-citas-paciente'),
    url(r'^citas-servicio-entidad/$', views.TotalCitasServicioEntidadView.as_view(), name='citas-servicio-entidad'),
    url(r'^tratamientos-pago-medicos/$', views.TratamientosPagoMedicosView.as_view(), name='tratamientos-pago-medicos'),
    url(r'^ind-mortalidad-morbilidad/$', views.IndMortalidadMorbilidadView.as_view(), name='ind-mortalidad-morbilidad'),
    url(r'^relacion-citas-profesional/$', views.RelacionCitasProfesionalView.as_view(), name='relacion-citas-profesional'),
    url(r'^tratamientos-pago-terapeutas/$',views.TratamientosPagoTerapeutasView.as_view(), name='tratamientos-pago-terapeutas'),
    url(r'^medicos-ordenan-tratamiento/$', views.ReporteMedicosOrdenanTratamientoView.as_view(), name='medicos-ordenan-tratamiento'),
    url(r'^citas-servicio-entidad-print/$', views.PrintTotalCitasServicioEntidadView.as_view(), name='citas-servicio-entidad-print'),
    url(r'^ind-mortalidad-morbilidad-print/$', views.PrintIndMortalidadMorbilidadView.as_view(), name='ind-mortalidad-morbilidad-print'),
    url(r'^tratamientos-facturados-entidad/$', views.TratamientosFacturadosEntidadView.as_view(), name='tratamientos-facturados-entidad'),
    url(r'^tratamientos-no-facturados-entidad/$', views.TratamientosNoFacturadosEntidadView.as_view(), name='tratamientos-no-facturados-entidad'),
    url(r'^tratamientos-iniciados-profesional/$', views.TratamientosIniciadosProfesionalView.as_view(), name='tratamientos-iniciados-profesional'),
    url(r'^tratamientos-no-terminados-profesional/$', views.TratamientosNoTerminadosProfesionalView.as_view(), name='tratamientos-no-terminados-profesional'),
]
