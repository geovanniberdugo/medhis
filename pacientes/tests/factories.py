import faker
import factory
import datetime
from .. import models


class PacienteFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Paciente

    primer_nombre = factory.Faker('first_name', locale='es')
    primer_apellido = factory.Faker('last_name', locale='es')
    genero = models.Paciente.FEMENINO
    fecha_nacimiento = factory.Faker('date_time_this_century', before_now=True)
    fecha_ingreso = factory.LazyFunction(datetime.datetime.now)
    tipo_documento = models.Paciente.CEDULA_CIUDADANIA
    numero_documento = factory.sequence(lambda n: '112343%02d' % n)
    estado_civil = models.Paciente.SOLTERO
    zona = models.Paciente.URBANO
    direccion = factory.Faker('address', locale='es')
    email = factory.Faker('email')
    lugar_nacimiento = factory.SubFactory('globales.tests.factories.PobladoFactory')
    lugar_residencia = factory.SubFactory('globales.tests.factories.PobladoFactory')

    # Datos responsable
    nombre_responsable = factory.Faker('name', locale='es')
    direccion_responsable = factory.Faker('address', locale='es')


class OrdenFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Orden

    paciente = factory.SubFactory(PacienteFactory)
    afiliacion = models.Orden.PARTICULAR
    tipo_usuario = models.Orden.PARTICULAR
    plan = factory.SubFactory('servicios.tests.factories.PlanFactory')
    institucion = factory.SubFactory('organizacional.tests.factories.InstitucionFactory')
    servicios = factory.RelatedFactory('pacientes.tests.factories.ServicioRealizarFactory', 'orden')
    acompanante = factory.RelatedFactory('pacientes.tests.factories.AcompananteFactory', 'orden')

class ServicioRealizarFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ServicioRealizar

    orden = factory.SubFactory(OrdenFactory)
    servicio = factory.SubFactory('servicios.tests.factories.ServicioFactory')
    valor = 10000
    coopago = 10000

class AcompananteFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Acompanante

    orden = factory.SubFactory(OrdenFactory, acompanante=None)
    nombre = factory.Faker('name', locale='es')
    direccion = factory.Faker('address', locale='es')
    telefono = 3049459
    
