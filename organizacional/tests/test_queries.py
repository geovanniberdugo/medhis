import pytest
import datetime
from unittest import mock
from django_dynamic_fixture import G, F
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Empleado, Sucursal, HorarioAtencion


class EmpleadoQueryTest(BaseGraphTestCase):

    def test_query(self):
        sucursal = G(Sucursal)
        user = UsuarioFactory()
        medico = G(Empleado, usuario=user, duracion_cita=datetime.timedelta(minutes=30))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=00), fin=datetime.time(hour=11, minute=00))
        self.login(user)

        response = self.query(
            '''
                query empleados($input: ID!){
                    empleados {
                        totalCount
                        results {
                            id
                            horasAtencion(sucursal: $input, fecha: "2019-11-11")
                        }
                    }
                }
            ''',
            op_name='empleados',
            input_data=sucursal.id
        )

        content = self.format_response(response)
        self.assertResponseNoErrors(response)
