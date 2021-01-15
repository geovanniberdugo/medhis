import pytest
import datetime
from django_dynamic_fixture import G, P
from common.tests.base import BaseTestCase
from agenda.models import Cita, HistorialEstado
from ..models import Empleado, HorarioAtencion, Sucursal, SinHorarioAtencion
from . import factories as fac

class EmpleadoModelTest(BaseTestCase):

    def test_horas_atencion_when_medico_sin_limite_atencion_simultanea(self):
        fecha1 = datetime.date(year=2019, month=11, day=11)
        fecha2 = datetime.date(year=2019, month=11, day=12)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30))
        horario = G(HorarioAtencion, medico=medico, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=00), fin=datetime.time(hour=10, minute=00))
        
        horas = medico.horas_atencion([fecha1, fecha2], horario.sucursal)
        assert horas == {
            fecha1: [
                datetime.time(8, 0),
                datetime.time(8, 30),
                datetime.time(9, 0),
                datetime.time(9, 30),
            ],
            fecha2: []
        }

    def test_horas_atencion_when_medico_con_limite_atencion_simultanea(self):
        fecha1 = datetime.date(year=2019, month=11, day=11)
        fecha2 = datetime.date(year=2019, month=11, day=12)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30), atenciones_simultaneas=1)
        horario = G(HorarioAtencion, medico=medico, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=00), fin=datetime.time(hour=11, minute=00))
        
        inicio = datetime.datetime.combine(fecha1, datetime.time(8, 0))
        cita1 = G(Cita, medico=medico, sucursal=horario.sucursal, inicio=inicio, fin=inicio + datetime.timedelta(minutes=30))
        cita1.actualizar_estado('NC', medico)
        cita2 = G(Cita, medico=medico, inicio=inicio + datetime.timedelta(minutes=30), fin=inicio + datetime.timedelta(minutes=60))
        cita2.actualizar_estado('NC', medico)
        cita3 = G(Cita, medico=medico, sucursal=horario.sucursal, inicio=inicio + datetime.timedelta(hours=1), fin=inicio + datetime.timedelta(hours=2))
        cita3.actualizar_estado('NC', medico)
        cita4 = G(Cita, medico=medico, sucursal=horario.sucursal, inicio=inicio + datetime.timedelta(hours=1), fin=inicio + datetime.timedelta(hours=2))
        cita4.actualizar_estado('NC', medico)

        horas = medico.horas_atencion([fecha1, fecha2], horario.sucursal)
        assert horas == {
            fecha1: [
                datetime.time(8, 30),
                datetime.time(10, 0),
                datetime.time(10, 30),
            ],
            fecha2: []
        }
    
    def test_horas_atencion_raises_exception_when_medico_no_tiene_horarios_atencion(self):
        sucursal = G(Sucursal)
        fecha1 = datetime.date(year=2019, month=11, day=11)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30), atenciones_simultaneas=1)

        with pytest.raises(SinHorarioAtencion):
            medico.horas_atencion([fecha1], sucursal)
