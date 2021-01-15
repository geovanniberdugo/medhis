from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField 
)
from .. import models


class SatisfaccionGlobal(DjangoObjectType):

    class Meta:
        model = models.SatisfaccionGlobal
        description = 'Definición de un registro de encuesta de satisfacción global'


class SatisfaccionGlobalList(DjangoListObjectType):

    class Meta:
        model = models.SatisfaccionGlobal
        description = 'Lista de registros de encuesta de satisfacción global'


class EventoAdverso(DjangoObjectType):

    class Meta:
        model = models.EventoAdverso
        description = 'Definicion de un evento adverso que puede suceder en la institucion'


class EventoAdversoList(DjangoListObjectType):

    class Meta:
        model = models.EventoAdverso
        description = 'Lista de Eventos Adversos que pueden suceder dentro de la institución'


class Query:
    satisfaccion_global = DjangoObjectField(SatisfaccionGlobal, description='Un solo registro satisfaccion global')
    lista_satisfaccion_global = DjangoListObjectField(SatisfaccionGlobalList, description='Lista todos los registros de satisfaccion global')
    evento_adverso = DjangoObjectField(EventoAdverso, description='Un solo evento adverso')
    eventos_adversos = DjangoListObjectField(EventoAdversoList, description='Lista todos los eventos adversos')
    