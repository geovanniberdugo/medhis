import pytest
from unittest import mock
from django.urls import reverse
from django_dynamic_fixture import G
from django.contrib.auth import get_user_model
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Institucion
from servicios.models import Cliente

User = get_user_model()

class FacturacionSiigoViewTest(BaseTestCase):

    URL = 'facturacion:siigo'
    PERMISSION = 'can_facturar'

    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL)
        self.response_302()

    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL)
        self.response_302()

    def test_user_with_permission_get_200(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL)
        self.response_200()
    
    def test_post_return_excel(self):
        cliente = G(Cliente)
        institucion = G(Institucion)
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        resp = self.post(self.URL, data={'institucion': institucion.id, 'desde': '01/10/2019', 'hasta': '31/10/2019', 'cliente': cliente.id})
        self.response_200()
        self.assertEqual(resp.get('content-type'), 'application/vnd.ms-excel')
