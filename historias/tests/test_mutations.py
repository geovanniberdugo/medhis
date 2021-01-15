import pytest
from unittest import mock
from django_dynamic_fixture import G, P, F
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Empleado
from ..models import Historia

class BorrarEncuentroMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        user = UsuarioFactory()
        historia = G(Historia, contenido={}, data={}, formato=F(contenido={}))
        self.login(user)

        _input = historia.id
        response = self.query(
            '''
                mutation BorrarEncuentro($input: ID!) {
                    borrarEncuentro(id: $input) {
                        ok
                        historia { id }
                    }
                }
            ''',
            op_name='BorrarEncuentro',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['borrarEncuentro']['ok']

class AbrirHistoriaMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        user = UsuarioFactory()
        historia = G(Historia, terminada=True, contenido={}, data={}, formato=F(contenido={}))
        self.login(user)

        _input = historia.id
        response = self.query(
            '''
                mutation AbrirHistoria($input: ID!) {
                    abrirHistoria(id: $input) {
                        historia { id }
                    }
                }
            ''',
            op_name='AbrirHistoria',
            input_data=_input
        )

        content = self.format_response(response)
        self.assertResponseNoErrors(response)
        assert content['data']['abrirHistoria']['historia'] is not None
