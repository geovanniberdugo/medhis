import graphene
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from graphene_django_extras import (
    DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField
)

UserM = get_user_model()

class Rol(DjangoObjectType):

    class Meta:
        model = Group
        description = 'Indican los permisos que tienen los usuarios'

class RolList(DjangoListObjectType):

    class Meta:
        model = Group

class User(graphene.ObjectType):

    id = graphene.ID(required=True)
    username = graphene.String(required=True)
    rol = graphene.Field(Rol)

    def resolve_rol(self, info, **kwargs):
        return self.groups.first()

class Query:
    roles = DjangoListObjectField(RolList, description='Lista de todos los roles')
