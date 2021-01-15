import pytest
import datetime
from django_dynamic_fixture import G, P
from organizacional.models import Institucion, Empleado, Sucursal
from common.tests.factories import UsuarioFactory
from common.tests.base import BaseGraphTestCase
from servicios.models import Plan, Servicio
from ..models import Cita

class AgendarCitaMutationTest(BaseGraphTestCase):

    def test_mutation_valid_save_cita(self):
        convenio = G(Plan)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        user = UsuarioFactory()
        institucion = G(Institucion)
        medico = G(Empleado, usuario=user)
        self.login(user)

        _input = {
            'estado': 'NC',
            'medico': medico.id,
            'sucursal': sucursal.id,
            'convenio': convenio.id,
            'servicio': servicio.id,
            'institucion': institucion.id,
            'duracion': '00:20:00',
            'fechaDeseada': '2019-11-12',
            'inicio': '2019-11-12T08:00:00.000-05:00',
            'paciente': {
                'genero': 'F',
                'telefono2': '',
                'primerNombre': 'NO',
                'celular': '3783558',
                'telefono': '3783558',
                'segundoApellido': '',
                'direccion': 'AUT DBG',
                'tipoDocumento': 'CC',
                'numeroDocumento': '1234',
                'segundoNombre': 'ASIGNAR',
                'primerApellido': 'CITA',
                'fechaNacimiento': '1988-08-04',
            },
        }
        response = self.query(
            '''
                mutation AgendarCita($input: AgendarCitaInput!) {
                    agendarCita(input: $input) {
                        ok
                        errors { field, messages }
                    }
                }
            ''',
            op_name='AgendarCita',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['agendarCita']['ok']

class AgregarAutorizacionCitaMutationTest(BaseGraphTestCase):

    def test_mutation_valid(self):
        cita = G(Cita)
        self.login(UsuarioFactory())

        _input = {
            'id': cita.id,
            'autorizacion': 'EWRDF2432',
            'autorizadoPor': 'Tania Hernadz',
            'fechaAutorizacion': '2019-11-14',
        }
        response = self.query(
            '''
                mutation AgregarAutorizacionCita($input: AgregarAutorizacionCitaInput!) {
                    agregarAutorizacionCita(input: $input) {
                        ok
                        errors { field, messages }
                    }
                }
            ''',
            op_name='AgregarAutorizacionCita',
            input_data=_input
        )

        content = self.format_response(response)
        print('..........')
        print(content)
        self.assertResponseNoErrors(response)
        assert content['data']['agregarAutorizacionCita']['ok']

class MoverCitaMutationTest(BaseGraphTestCase):

    def test_mutation_valid(self):
        cita = G(Cita)
        sucursal = G(Sucursal)
        user = UsuarioFactory()
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30))
        cita.actualizar_estado('NC', medico)
        self.login(user)

        _input = {
            'id': cita.id,
            'medico': medico.id,
            'sucursal': sucursal.id,
            'inicio': '2019-11-14T07:00:00.000-05:00'
        }
        response = self.query(
            '''
                mutation MoverCita($input: CitaUpdateGenericType!) {
                    moverCita(input: $input) {
                        ok
                        errors { field, messages }
                    }
                }
            ''',
            op_name='MoverCita',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['moverCita']['ok']
