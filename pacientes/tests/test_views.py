import pytest
from unittest import mock
from django.test import tag
from django_dynamic_fixture import G
from django.contrib.auth import get_user_model
from common.tests.factories import UsuarioFactory
from common.tests.base import BaseTestCase
from ..models import Orden, Paciente
from . import factories as fac

User = get_user_model()

class HistoriasSesionViewTest(BaseTestCase):
    
    URL = 'pacientes:historias-sesion'
    PERMISSION = 'add_historia'

    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_with_correct_permission_but_sesion_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL, pk=1)
        self.response_404()

class NuevaHistoriaSesionViewTest(BaseTestCase):
    
    URL = 'pacientes:nueva-historia'
    PERMISSION = 'add_historia'

    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL, pk=1, formato_pk=1)
        self.response_302()
    
    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL, pk=1, formato_pk=1)
        self.response_302()
    
    def test_user_with_correct_permission_but_sesion_formato_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL, pk=1, formato_pk=1)
        self.response_404()

class HistoriasPacienteViewTest(BaseTestCase):

    URL = 'pacientes:historias'
    PERMISSION = 'can_see_historias'

    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_with_correct_permission_but_paciente_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL, pk=1)
        self.response_404()

    def test_user_with_correct_permission_but_paciente_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        paciente = G(Paciente)
        self.get(self.URL, pk=paciente.id)
        self.response_200()
    