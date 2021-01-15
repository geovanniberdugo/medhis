import pytest
from django_dynamic_fixture import G
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Empleado
from ..models import Factura

class AnularFacturaMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        user = UsuarioFactory()
        G(Empleado, usuario=user)
        factura = G(Factura)
        self.login(user)

        razon = 'probando'
        _input = {
            'id': factura.id,
            'razonAnulacion': razon
        }
        response = self.query(
            '''
                mutation AnularFactura($input: AnularFacturaInput!) {
                    anularFactura(input: $input) {
                        ok
                        factura {
                            id
                            razonAnulacion
                            anuladoEl @date(format: "DD/MM/YYYY")
                            anuladoPor {
                                id
                                nombreCompleto @title_case
                            }
                        }
                    }
                }
            ''',
            op_name='AnularFactura',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['anularFactura']['ok']
        assert content['data']['anularFactura']['factura']['razonAnulacion'] == razon

class EliminarFacturaMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        user = UsuarioFactory()
        factura = G(Factura)
        self.login(user)

        _input = factura.id
        response = self.query(
            '''
                mutation EliminarFactura($input: ID!) {
                    eliminarFactura(id: $input) {
                        ok
                        factura {
                            id
                        }
                    }
                }
            ''',
            op_name='EliminarFactura',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['eliminarFactura']['ok']
        assert content['data']['eliminarFactura']['factura']['id'] == str(factura.id)

