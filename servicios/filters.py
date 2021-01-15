import django_filters
from organizacional.models import Institucion
from . import models


class ServicioFilter(django_filters.FilterSet):
    """Filtro para el modelo servicio."""

    institucion = django_filters.ModelChoiceFilter(
        field_name='tarifas__institucion',
        queryset=Institucion.objects.all()
    )

    class Meta:
        model = models.Servicio
        fields = ['planes', 'institucion']

class PlanFilter(django_filters.FilterSet):
    """Filtro para el modelo plan."""

    institucion = django_filters.ModelChoiceFilter(
        distinct=True,
        field_name='tarifas__institucion',
        queryset=Institucion.objects.all()
    )

    class Meta:
        model = models.Plan
        fields = ['institucion', 'cliente']
