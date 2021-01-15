import factory
from .. import models

class CitaFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Agenda
