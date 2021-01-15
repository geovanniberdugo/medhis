import pytest
import datetime
from unittest import mock
from django_dynamic_fixture import G, P
from common.tests.base import BaseGraphTestCase
from common.tests.factories import UsuarioFactory
from organizacional.models import Empleado, Sucursal, HorarioAtencion
from ..models import Tratamiento, Orden
from servicios.models import Servicio
from agenda.models import Cita

class EditarTratamientoMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        user = UsuarioFactory()
        sucursal = G(Sucursal)
        medico = G(Empleado, usuario=user, duracion_cita=datetime.timedelta(minutes=30))
        tratamiento = G(Tratamiento, cantidad=1)
        fecha = datetime.datetime(year=2019, month=11, day=11, hour=8, minute=0)
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.MARTES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        cita = G(Cita, servicio_prestado=tratamiento, medico=medico, inicio=fecha, sucursal=sucursal)
        cita.actualizar_estado('NC', medico)
        self.login(user)

        _input = {
            'cantidad': 3,
            'valor': 31100,
            'coopago': 10000,
            'isUnaCita': False,
            'id': tratamiento.id,
            'isCoopagoTotal': False,
            'numSesionesCoopago': None,
            'servicio': tratamiento.servicio_id,
        }
        response = self.query(
            '''
                mutation ActualizarTratamiento($input: EditarTratamientoInput!) {
                    editarTratamiento(input: $input) {
                        ok
                        errors { field, messages }
                    }
                }
            ''',
            op_name='ActualizarTratamiento',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['editarTratamiento']['ok']

class AgregarServicioOrdenMutationTest(BaseGraphTestCase):

    def test_valid_mutation(self):
        orden = G(Orden)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        user = UsuarioFactory()
        medico = G(Empleado, usuario=user, tipo=Empleado.MEDICO, duracion_cita=datetime.timedelta(minutes=30))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.MARTES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        self.login(user)

        _input = {
            'cantidad': '1',
            'orden': orden.id,
            'coopago': '10000',
            'medico': medico.id,
            'duracion': '00:20:00',
            'autorizacion': '3122',
            'sucursal': sucursal.id,
            'servicio': servicio.id,
            'fechaAutorizacion': '2019-11-17',
            'fecha': '2019-11-11T08:00:00.000-05:00',
        }
        response = self.query(
            '''
                mutation AgregarServicioOrden($input: AddServicioOrdenInput!){
                    agregarServicioOrden(input: $input) {
                        ok
                        errors { field, messages }
                    }
                }
            ''',
            op_name='AgregarServicioOrden',
            input_data=_input
        )

        self.assertResponseNoErrors(response)
        content = self.format_response(response)
        assert content['data']['agregarServicioOrden']['ok']
