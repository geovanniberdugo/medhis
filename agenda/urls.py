from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AgendaDiariaView.as_view(), name='listar'),
    url(r'^citas/$', views.AgendaCitasView.as_view(), name='citas'),
    url(r'^imprimir/$', views.PrintAgendaDiariaView.as_view(), name='print'),
    url(r'^indicadores/$', views.IndicadoresResolucion256View.as_view(), name='indicadores-resolucion-256'),
    url(r'^tipos-agenda/$', views.ListarTiposAgendaView.as_view(), name='listar-tipos-agenda'),
]
