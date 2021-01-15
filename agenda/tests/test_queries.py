import pytest
from django_dynamic_fixture import G, F
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from ..models import Cita


@pytest.mark.actual
class OrdenQueryTest(BaseGraphTestCase):

    def test_query(self):
        cita = G(Cita)
        self.login(UsuarioFactory())

        response = self.query(
            '''
                query cita($input: ID!){
                    cita(id: $input) {
                        id
                        inicio
                        canEdit
                        canMove
                        autorizacion
                        autorizadoPor
                        fechaAutorizacion
                        historialActual { id }
                        sucursal { id, nombre @title_case }
                        medico { id, nombreCompleto @title_case }
                    }
                }
            ''',
            op_name='cita',
            input_data=cita.id
        )

        content = self.format_response(response)
        print('..........')
        print(content)
        self.assertResponseNoErrors(response)
