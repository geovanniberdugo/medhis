import pytest
import datetime
from django.test import tag
from freezegun import freeze_time
from django_dynamic_fixture import N, G
from common.tests.base import BaseTestCase
from organizacional.models import Empleado, HorarioAtencion, Sucursal
from agenda.models import Cita, HistorialEstado
from ..models import Tratamiento
from . import factories as fac
from .. import models as m

@pytest.mark.actual
class PacienteModelTest(BaseTestCase):
    """Pruebas unitarias para el modelo Paciente."""

    def setUp(self):
        self.paciente = fac.PacienteFactory()

    def test_ultimo_acompanante_returns_None(self):
        """Prueba que si un paciente no tiene ninguna orden asociada el acompañante sea None."""

        self.assertIsNone(self.paciente.ultimo_acompanante)

    def test_edad_actual_paciente(self):
        paciente = fac.PacienteFactory.build(fecha_nacimiento=datetime.date(2010, 1, 10))

        with freeze_time("2018-01-20"):
            edad = paciente.edad

        self.assertEqual(edad, "8 Años")
    
    def test_edad_relativa_years(self):
        paciente = fac.PacienteFactory.build(fecha_nacimiento=datetime.date(2010, 1, 10))
        assert paciente.edad_relativa(datetime.date(2018, 1, 20)) == '8 Años'

    def test_edad_relativa_months(self):
        paciente = fac.PacienteFactory.build(fecha_nacimiento=datetime.date(2018, 3, 10))
        assert paciente.edad_relativa(datetime.date(2018, 1, 20)) == '2 Meses'

    def test_edad_relativa_days(self):
        paciente = fac.PacienteFactory.build(fecha_nacimiento=datetime.date(2018, 1, 10))
        assert paciente.edad_relativa(datetime.date(2018, 1, 20)) == '10 Dias'

class TratamientoModelTest(BaseTestCase):

    def test_reagendar_cita_crea_cantidad_citas(self):
        sucursal = G(Sucursal)
        tratamiento = G(Tratamiento, cantidad=1)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        cita = G(Cita, servicio_prestado=tratamiento, sucursal=sucursal, medico=medico)
        cita.actualizar_estado('NC', medico)

        tratamiento.reagendar_citas(medico, 2)
        assert tratamiento.citas.count() == 3

    def test_reagendar_cita_crea_cantidad_citas(self):
        sucursal = G(Sucursal)
        tratamiento = G(Tratamiento, cantidad=2)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        cita = G(Cita, servicio_prestado=tratamiento, sucursal=sucursal, medico=medico)
        cita.actualizar_estado('NC', medico)
        cita = G(Cita, servicio_prestado=tratamiento, sucursal=sucursal, medico=medico)
        cita.actualizar_estado('EX', medico)

        tratamiento.reagendar_citas(medico)
        assert tratamiento.citas.count() == 3

def test_coopago_total_when_por_sesion():
    tratamiento = N(Tratamiento, is_coopago_total=False, cantidad=2, coopago=10000, persist_dependencies=False)
    assert tratamiento.coopago_total == 20000

def test_coopago_total_when_set_todas_sesiones():
    tratamiento = N(Tratamiento, is_coopago_total=True, cantidad=2, coopago=10000, persist_dependencies=False)
    assert tratamiento.coopago_total == 10000

def test_coopago_total_when_set_num_sesiones_especificas():
    tratamiento = N(Tratamiento, num_sesiones_coopago=6, cantidad=10, coopago=10000, persist_dependencies=False)
    assert tratamiento.coopago_total == 20000
