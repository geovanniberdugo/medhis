from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^graphql2/$', views.CustomGraphQLView.as_view(), name='graphql2'),
    url(r'^graphql/$', views.CustomGraphQLView.as_view(batch=True), name='graphql'),
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^graphiql/$', views.CustomGraphQLView.as_view(graphiql=True)),
    ] + urlpatterns
