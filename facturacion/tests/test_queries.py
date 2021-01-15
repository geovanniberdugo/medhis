import pytest
from django_dynamic_fixture import G
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from ..models import Factura

class FacturasQueryTest(BaseGraphTestCase):

    def test_query(self):
        user = UsuarioFactory()
        G(Factura)
        G(Factura)
        self.login(user)

        response = self.query(
            '''
                query {
                    facturas {
                        totalCount
                        results {
                            id
                            total
                            numero
                            fechaFin
                            canAnular
                            detalleUrl
                            fechaInicio
                            canEliminar
                            razonAnulacion
                            fechaExpedicion
                            anuladoEl @date(format: "DD/MM/YYYY")
                            anuladoPor { id, nombreCompleto @title_case }
                        }
                    }
                }
            ''',
            op_name='facturas'
        )

        content = self.format_response(response)
        print(content)
        self.assertResponseNoErrors(response)
