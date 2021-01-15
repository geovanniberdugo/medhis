import factory
from .. import models


class FacturaFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Factura
    
    numero = factory.sequence(lambda n: '00%02d' % n)
