import datetime
from django.test import tag
from django.utils import timezone
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from organizacional.tests.factories import MedicoFactory, SucursalFactory


class ListarTiposAgendaViewTest(BaseTestCase):

    URL = 'agenda:listar-tipos-agenda'

    def setUp(self):
        self.login(UsuarioFactory(user_permissions=['add_agenda']))
    
    def test_get_returns_200(self):
        self.get_check_200(self.URL)
