from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField 
)
from .. import models
from .. import filters

class Municipio(DjangoObjectType):

    class Meta:
        model = models.Municipio

class Poblado(DjangoObjectType):

    class Meta:
        model = models.Poblado

class PobladoList(DjangoListObjectType):

    class Meta:
        model = models.Poblado
        filterset_class = filters.PobladoFilter


class CodigoCie(DjangoObjectType):

    class Meta:
        model = models.Cie

class CodigoCieList(DjangoListObjectType):

    class Meta:
        model = models.Cie
        description = 'Lista de codigo de diagnostico (CIE10)'
        filterset_class = filters.CieFilter

class Profesion(DjangoObjectType):

    class Meta:
        model = models.Profesion

class ProfesionList(DjangoListObjectType):

    class Meta:
        model = models.Profesion


class Query:
    codigos_cie = DjangoListObjectField(CodigoCieList, description='Lista todos los codigos de diagnostico (CIE10)')
    codigo_cie = DjangoObjectField(CodigoCie, description='Un solo codigo de diagnostico (CIE10)')
    profesiones = DjangoListObjectField(ProfesionList, description='Lista todos las profesiones')
    poblados = DjangoListObjectField(PobladoList, description='Lista todos los poblados')
    poblado = DjangoObjectField(Poblado, description='Un solo poblado')
