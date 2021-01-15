from unittest import mock
from django.test import tag
from django.contrib.auth import get_user_model
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory

User = get_user_model()

class ListarServiciosViewTest(BaseTestCase):

    URL = 'servicios:listar'

    def setUp(self):
        self.login(UsuarioFactory(user_permissions=['add_servicio']))

    def test_get_returns_200(self):
        self.get_check_200(self.URL)

class ListarClientesViewTest(BaseTestCase):

    URL = 'servicios:listar-clientes'
    
    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL)
        self.response_302()

    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL)
        self.response_302()
    
    def test_user_with_permission_add_cliente_get_200(self):
        self.login(UsuarioFactory(user_permissions=['add_cliente']))
        self.get_check_200(self.URL)

class ListarPlanesViewTest(BaseTestCase):

    URL = 'servicios:listar-planes'
    
    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL, pk=1)
        self.response_302()

    def test_user_with_correct_permission_but_cliente_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=['add_plan']))
        self.get(self.URL, pk=1)
        self.response_404()
    
    @mock.patch('servicios.views.DetailView.get_object', return_value=mock.Mock())
    def test_user_with_permission_add_plan_get_200(self, mock_get_object):
        self.login(UsuarioFactory(user_permissions=['add_plan']))
        self.get_check_200(self.URL, pk=1)

