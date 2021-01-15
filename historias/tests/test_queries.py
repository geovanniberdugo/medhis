import pytest
from unittest import mock
from django_dynamic_fixture import G, F
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Empleado
from ..models import Historia

class HistoriaQueryTest(BaseGraphTestCase):

    @mock.patch('historias.utils.flatten_medical_record', autospec=True, return_value=[])
    def test_query(self, mock_flatten):
        user = UsuarioFactory()
        G(Empleado, usuario=user)
        G(Historia, contenido={}, data={}, formato=F(contenido={}))
        G(Historia, contenido={}, data={}, formato=F(contenido={}))
        self.login(user)

        response = self.query(
            '''
                query {
                    historias {
                        totalCount
                        results {
                            id
                            canAbrir
                            printUrl
                            detailUrl
                            canDelete
                            printContent
                            formato { id, nombre @title_case }
                            adjuntos { id, archivo { nombre, url } }
                            medico: proveedor { id, nombreCompleto @title_case }
                            cita {
                                id
                                inicio
                                servicio { id, nombre @title_case }
                            }
                        }
                    }
                }
            ''',
            op_name='historias'
        )

        content = self.format_response(response)
        self.assertResponseNoErrors(response)
