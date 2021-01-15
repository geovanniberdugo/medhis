from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pacientes-tratamientos-finalizados/$', views.PacientsTerminaronTratamiento.as_view(), name='pacientes-terminaron-tratamientos'),
]
