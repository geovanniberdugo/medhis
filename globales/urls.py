from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cies/$', views.ListarCiesView.as_view(), name='cies')
]