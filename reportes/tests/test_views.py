import pytest
from unittest import mock
from django.contrib.auth import get_user_model
from common.tests.factories import UsuarioFactory
from common.tests.base import BaseTestCase

User = get_user_model()

class TratamientosNoFacturadosEntidadViewTest(BaseTestCase):

    URL = 'reportes:tratamientos-no-facturados-entidad'
    PERMISSION = 'can_see_tratamientos_no_facturados_entidad'

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
