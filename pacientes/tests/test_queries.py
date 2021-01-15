import pytest
from django_dynamic_fixture import G, F
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from ..models import Tratamiento, Orden
from agenda.models import Cita

class TratamientosQueryTest(BaseGraphTestCase):

    def test_query(self):
        tratamiento = G(Tratamiento)
        G(Cita, servicio_prestado=tratamiento)
        self.login(UsuarioFactory())

        response = self.query(
            '''
                query tratamientos{
                    tratamientos {
                        totalCount
                        results {
                            id
                            ordenUrl
                            orden { id }
                            fechaFinTratamiento
                            fechaInicioTratamiento
                            servicio { id, nombre @title_case }
                            paciente {
                                id
                                tipoDocumento
                                numeroDocumento
                                nombreCompleto @title_case
                            }
                        }
                    }
                }
            ''',
            op_name='tratamientos'
        )

        content = self.format_response(response)
        self.assertResponseNoErrors(response)

@pytest.mark.actual
class OrdenQueryTest(BaseGraphTestCase):

    def test_query(self):
        orden = G(Orden)
        self.login(UsuarioFactory())

        response = self.query(
            '''
                query orden($input: ID!){
                    orden(id: $input) {
                        id
                        canEdit
                        afiliacion
                        tipoUsuario
                        afiliacionLabel
                        tipoUsuarioLabel
                        asistioAcompanante
                        medicoOrdena @title_case
                        institucion { id, nombre @title_case }
                        tratamientos: serviciosRealizar { id }
                        convenio: plan { 
                            id
                            requiereAutorizacion
                            nombreCompleto @title_case
                        }
                        paciente { id }
                        acompanante {
                            id
                            nombre
                            telefono
                            direccion
                            parentesco
                            parentescoLabel
                        }
                    }
                }
            ''',
            op_name='orden',
            input_data=orden.id
        )

        content = self.format_response(response)
        self.assertResponseNoErrors(response)
