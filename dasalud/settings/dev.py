import os
import socket
from .base import *

#  Apps

TENANT_APPS += [
    'silk',
]

SHARED_APPS += [
    'debug_toolbar',
    'debug_panel',
    'django_extensions',
]

INSTALLED_APPS = SHARED_APPS + list(set(TENANT_APPS) - set(SHARED_APPS))

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'debug_panel.middleware.DebugPanelMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'common.middleware.IPAccessMiddleware',
    'common.middleware.TimeBasedAccessMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1']

# Shell plus

SHELL_PLUS_POST_IMPORTS = [
    ('pacientes.serializers', '*'),
    ('agenda.serializers', '*')
]
