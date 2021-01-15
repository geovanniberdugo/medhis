import pytest
import datetime
from django_dynamic_fixture import G, N
from common.tests.base import BaseTestCase
from organizacional.models import Empleado, Sucursal
from ..models import Cita

def test_duracion_cita():
    duracion = datetime.timedelta(minutes=30)
    fecha = datetime.datetime(year=2019, month=12, day=1, hour=8, minute=0)
    cita = N(Cita, inicio=fecha, fin=fecha + duracion, persist_dependencies=False)

    assert cita.duracion == duracion

class CitaModelTest(BaseTestCase):

    def test_mover_cita(self):
        nueva_fecha = datetime.datetime(year=2019, month=12, day=1, hour=8, minute=0)
        inicio = datetime.datetime(year=2019, month=11, day=1, hour=8, minute=0)
        cita = G(Cita, inicio=inicio, fin=inicio + datetime.timedelta(minutes=30))
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=10))
        sucursal = G(Sucursal)

        n_cita = cita.mover_cita(medico=medico, sucursal=sucursal, inicio=nueva_fecha)
        assert n_cita.inicio == nueva_fecha
        assert n_cita.medico_id == medico.id
        assert n_cita.sucursal_id == sucursal.id

        fin_cita = nueva_fecha + datetime.timedelta(minutes=30)
        assert n_cita.fin == fin_cita
