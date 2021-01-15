import factory
from .. import models


class TipoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Tipo
        django_get_or_create = ('nombre', )
    
    nombre = 'CONSULTAS'


class ServicioFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Servicio
        django_get_or_create = ('nombre', )
    
    nombre = 'CONSULTA PRIMERA VEZ'
    codigo = factory.sequence(lambda n: '123456%02d' % n)
    abreviatura = 'CPV'
    tipo = factory.SubFactory(TipoFactory)


class ClienteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Cliente
        django_get_or_create = ('nombre', )
    
    nombre = 'PARTICULAR'
    razon_social = 'PARTICULAR'
    nit = factory.sequence(lambda n: '123456%02d' % n)


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Plan
        django_get_or_create = ('nombre', )
    
    nombre = 'PARTICULAR'
    cliente = factory.SubFactory(ClienteFactory)


class TarifaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Tarifa
    
    plan = factory.SubFactory(PlanFactory)
    servicio = factory.SubFactory(ServicioFactory)
    valor = 10000