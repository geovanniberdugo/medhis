"""dasalud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

from graphene_django_extras.views import ExtraGraphQLView

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^', include(('common.urls', 'common'), namespace='common')),
    url(r'^agenda/', include(('agenda.urls', 'agenda'), namespace='agenda')),
    url(r'^globales/', include(('globales.urls', 'globales'), namespace='globales')),
    url(r'^historias/', include(('historias.urls', 'historias'), namespace='historias')),
    url(r'^pacientes/', include(('pacientes.urls', 'pacientes'), namespace='pacientes')),
    url(r'^servicios/', include(('servicios.urls', 'servicios'), namespace='servicios')),
    url(r'^encuestas/', include(('encuestas.urls', 'encuestas'), namespace='encuestas')),
    url(r'^reportes/', include(('reportes.urls', 'reportes'), namespace='reportes')),
    url(r'^auditorias/', include(('auditorias.urls', 'auditorias'), namespace='auditorias')),
    url(r'^organizacional/', include(('organizacional.urls', 'organizacional'), namespace='organizacional')),
    url(r'^facturacion/', include(('facturacion.urls', 'facturacion'), namespace='facturacion')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
