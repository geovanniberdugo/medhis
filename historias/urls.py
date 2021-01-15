from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.DetailHistoriaView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/imprimir/$', views.PrintHistoriaView.as_view(), name='print'),
    url(r'^(?P<sesion>\d+)/(?P<formato>\d+)/adjuntos/$',views.NewEncounterAdjuntosView.as_view(), name='new-encounter-adjuntos'),
    url(r'^(?P<pk>\d+)/adjuntos/$',views.AdjuntosEncuentroView.as_view(), name='adjuntos'),

    url(r'^adjuntos/(?P<pk>\d+)/eliminar/$',
        views.AdjuntosHistoriaDestroyView.as_view(), name='adjuntos-eliminar'),
    url(r'^formatos/$', views.FormatoView.as_view()),
    url(r'^list/$', views.HistoriaView.as_view())
]
