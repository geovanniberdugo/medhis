import pytest
import datetime
from unittest import mock
from django.utils import timezone
from django_dynamic_fixture import N, G, F
from common.tests.base import BaseTestCase
from django.forms.models import model_to_dict
from organizacional.models import Institucion, Empleado, Sucursal, HorarioAtencion
from pacientes.models import Paciente, Orden, Tratamiento
from servicios.models import Plan, Servicio
from agenda.models import Cita
from .. import services as s

@pytest.mark.actual
class AgregarAutorizacionTest(BaseTestCase):

    def test_agrega_autorizacion_a_cita(self):
        cita = G(Cita)
        aut = 'SDFSF343'
        autorizado_por = 'Maria Mendoza'
        fecha_autorizacion = datetime.date(2020, 1, 1)
        
        s.agregar_autorizacion(cita, aut, fecha_autorizacion, autorizado_por)
        cita.refresh_from_db()
        assert cita.autorizacion == aut
        assert cita.autorizado_por == autorizado_por
        assert cita.fecha_autorizacion == fecha_autorizacion
    
    def test_agrega_autorizacion_sin_autorizado_por(self):
        cita = G(Cita)
        aut = 'SDFSF343'
        fecha_autorizacion = datetime.date(2020, 1, 1)

        s.agregar_autorizacion(cita, aut, fecha_autorizacion)
        cita.refresh_from_db()
        assert cita.autorizacion == aut
        assert cita.autorizado_por == ''
        assert cita.fecha_autorizacion == fecha_autorizacion

    def test_agregar_autorizacion_todas_citas_si_aplica_todas(self):
        tratamiento = G(Tratamiento, orden=F(plan=F(sesiones_autorizacion=0)))
        cita = G(Cita, servicio_prestado=tratamiento)
        cita1 = G(Cita, servicio_prestado=tratamiento)

        aut = 'SDFSF343'
        autorizado_por = 'Maria Mendoza'
        fecha_autorizacion = datetime.date(2020, 1, 1)

        s.agregar_autorizacion(cita, aut, fecha_autorizacion, autorizado_por)

        cita.refresh_from_db()
        cita1.refresh_from_db()
        assert cita.autorizacion == aut
        assert cita.autorizado_por == autorizado_por
        assert cita.fecha_autorizacion == fecha_autorizacion
        assert cita1.autorizacion == aut
        assert cita1.autorizado_por == autorizado_por
        assert cita1.fecha_autorizacion == fecha_autorizacion

class AgendarCitaTest(BaseTestCase):
    
    def test_agendar_cita_guarda_cita(self):
        convenio = G(Plan)
        medico = G(Empleado)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        inicio = timezone.now()
        institucion = G(Institucion)
        duracion = datetime.timedelta(minutes=30)
        paciente_data = model_to_dict(N(Paciente))
        cita = s.agendar_cita(paciente_data, 'NC', medico, institucion, servicio, convenio, medico, inicio, duracion, sucursal)

        assert Cita.objects.count() == 1
        assert Orden.objects.count() == 1
    
    def test_agendar_cita_crea_paciente_si_no_existe(self):
        convenio = G(Plan)
        medico = G(Empleado)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        inicio = timezone.now()
        institucion = G(Institucion)
        duracion = datetime.timedelta(minutes=30)
        paciente_data = model_to_dict(N(Paciente, numero_documento='1234'))
        cita = s.agendar_cita(paciente_data, 'NC', medico, institucion, servicio, convenio, medico, inicio, duracion, sucursal)

        assert Paciente.objects.get(numero_documento='1234')

    def test_agendar_cita_no_crea_paciente_si_existe(self):
        convenio = G(Plan)
        medico = G(Empleado)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        inicio = timezone.now()
        institucion = G(Institucion)
        duracion = datetime.timedelta(minutes=30)
        paciente = G(Paciente, numero_documento='1234')
        cita = s.agendar_cita(model_to_dict(paciente), 'NC', medico, institucion, servicio, convenio, medico, inicio, duracion, sucursal)

        assert Paciente.objects.count() == 1
        assert cita.paciente.id == paciente.id
    
    def test_agendar_cita_sets_autorizacion_convenio_no_requiere_autorizacion(self):
        medico = G(Empleado)
        servicio = G(Servicio)
        sucursal = G(Sucursal)
        inicio = timezone.now()
        institucion = G(Institucion)
        duracion = datetime.timedelta(minutes=30)
        convenio = G(Plan, cliente=F(sesiones_autorizacion=0))
        paciente_data = model_to_dict(N(Paciente, numero_documento='1234'))
        cita = s.agendar_cita(paciente_data, 'NC', medico, institucion, servicio, convenio, medico, inicio, duracion, sucursal)

        cita.refresh_from_db()
        assert cita.autorizacion == 'AU{}'.format(cita.servicio_prestado.orden.id)

class AgendarMultiplesCitasTest(BaseTestCase):

    def test_agendar_mutliples_citas(self):
        sucursal = G(Sucursal)
        tratamiento = G(Tratamiento)
        hora = datetime.time(hour=8, minute=00)
        duracion = datetime.timedelta(minutes=30)
        desde = datetime.date(year=2019, month=11, day=11)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=30))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.MARTES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        citas = s.agendar_multiples_citas(2, desde, hora, duracion, medico, sucursal, tratamiento, medico)

        assert len(citas) == 2
        assert citas[0].inicio == datetime.datetime.combine(desde, datetime.time(8, 0))
        assert citas[1].inicio == datetime.datetime.combine(desde + datetime.timedelta(days=1), datetime.time(8, 0))

    def test_agendar_mutliples_citas_duracion_correcta(self):
        sucursal = G(Sucursal)
        tratamiento = G(Tratamiento)
        hora = datetime.time(hour=8, minute=00)
        duracion = datetime.timedelta(minutes=30)
        desde = datetime.date(year=2019, month=11, day=5)
        medico = G(Empleado, duracion_cita=datetime.timedelta(minutes=10))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.LUNES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        G(HorarioAtencion, medico=medico, sucursal=sucursal, dia=HorarioAtencion.MARTES, inicio=datetime.time(hour=8, minute=0), fin=datetime.time(hour=11, minute=0))
        citas = s.agendar_multiples_citas(2, desde, hora, duracion, medico, sucursal, tratamiento, medico)

        assert citas[0].duracion == duracion
        assert citas[1].duracion == duracion
