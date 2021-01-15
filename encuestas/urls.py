from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^satisfaccion-global/$', views.CrearSatisfaccionGlobalView.as_view(), name='satisfaccion-global'),
]