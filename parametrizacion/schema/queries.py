from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField
)
from .. import models


class ParametrizacionRips(DjangoObjectType):

    class Meta:
        model = models.Rips
        description = 'Indica los valores por defecto de los rips'

class ParametrizacionRipsList(DjangoListObjectType):

    class Meta:
        model = models.Rips
        filter_fields = ['tipo']

class Query:
    parametro_rips = DjangoObjectField(ParametrizacionRips, description='Un solo parametro rips')
    parametros_rips = DjangoListObjectField(ParametrizacionRipsList, description='Lista de parametros para los rips')
