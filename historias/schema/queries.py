import graphene
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoListObjectField, DjangoObjectField
)
from django.urls import reverse
from .. import filters
from .. import models
from .. import utils


class Formato(DjangoObjectType):

    class Meta:
        model = models.Formato
        description = 'Son los distintos formatos para las historias.'

class FormatoList(DjangoListObjectType):

    class Meta:
        model = models.Formato
        description = 'Definición del tipo para una lista de formatos.'
        filterset_class = filters.FormatoFilter

class Archivo(graphene.ObjectType):

    url = graphene.String(required=True)
    nombre = graphene.String(required=True)

    def resolve_url(self, info):
        return self.url

    def resolve_nombre(self, info):
        return self.name.split('/')[-1]

class Adjunto(DjangoObjectType):

    archivo = graphene.Field(Archivo, required=True)

    class Meta:
        model = models.Adjunto

    def resolve_archivo(self, info, **kwarg):
        return self.archivo

class Historia(DjangoObjectType):

    can_abrir = graphene.Boolean(description='Indica si puede abrir el encuentro')
    can_edit = graphene.Boolean(description='Indica si puede editar el encuentro')
    can_delete = graphene.Boolean(description='Indica si puede borrar el encuentro')
    print_content = graphene.JSONString(description='Contenido de la historia para imprimir')
    print_url = graphene.String(source='print_url', description='URL para la impresión del encuentro')
    detail_url = graphene.String(source='get_absolute_url', description='URL del detalle del encuentro')
    adjuntos_url = graphene.String(source='adjuntos_url', description='URL de los adjuntos del encuentro')
    visita_url = graphene.String(source='visita_url', description='URL de la visita a la cual se encuentra asociada el encuentro')

    class Meta:
        model = models.Historia
        description = 'Una historia guarda la información medica de un paciente'
    
    def resolve_can_abrir(self, info, **kwargs):
        return self.can_abrir(info.context.user)

    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)
    
    def resolve_can_delete(self, info, **kwargs):
        return self.can_delete(info.context.user)

    def resolve_print_content(self, info, **kwargs):
        return info.context.dataloaders.print_content_by_historia.load(self.id)

    def resolve_proveedor(self, info, **kwargs):
        return info.context.dataloaders.proveedor_by_historia.load(self.id)

    def resolve_formato(self, info, **kwargs):
        return info.context.dataloaders.formato_by_historia.load(self.id)


class HistoriaList(DjangoListObjectType):

    class Meta:
        model = models.Historia
        description = 'Definición del tipo de una lista de historias'
        filterset_class = filters.HistoriaFilter


class Query:
    historias = DjangoListObjectField(HistoriaList, description='Lista de todas las historias')
    formatos = DjangoListObjectField(FormatoList, description='Lista de todos los formatos')
    encuentro = DjangoObjectField(Historia, description='Un solo encuentro')
    formato = DjangoObjectField(Formato, description='Un solo formato')
