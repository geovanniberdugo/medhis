import graphene
from graphene_django_extras.converter import convert_django_field
from graphene_django_extras.utils import is_required
from django.db import models
from .types import LocalCustomDateTime

@convert_django_field.register(models.DurationField)
def convert_field_to_string(field, registry=None, input_flag=None, nested_field=False):
    return graphene.String(
        description=field.help_text or field.verbose_name,
        required=is_required(field) and input_flag == 'create'
    )

@convert_django_field.register(models.DateTimeField)
def convert_date_to_string(field, registry=None, input_flag=None, nested_field=False):
    return LocalCustomDateTime(
        description=field.help_text or field.verbose_name,
        required=is_required(field) and input_flag == 'create'
    )
