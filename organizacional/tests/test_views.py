from unittest import mock
from django.test import tag
from django.urls import reverse
from rest_framework import status
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from . import factories as fac

class ListarSucursalesViewTest(BaseTestCase):

    URL = 'organizacional:listar-sucursales'

    def setUp(self):
        self.login(UsuarioFactory(user_permissions=['add_sucursal']))
    
    def test_get_returns_200(self):
        self.get_check_200(self.URL)


class ListarInstitucionesViewTest(BaseTestCase):

    URL = 'organizacional:listar-instituciones'

    def setUp(self):
        self.login(UsuarioFactory(user_permissions=['add_institucion']))
    def test_get_returns_200(self):
        self.get_check_200(self.URL)
