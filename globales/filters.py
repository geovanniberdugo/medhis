import django_filters
from . import models


class CieFilter(django_filters.FilterSet):
    """Filtro para los codigos de diagnostico (CIE10)."""

    search = django_filters.CharFilter(method='search_code')

    class Meta:
        model = models.Cie
        fields = ['search']
    
    def search_code(self, queryset, name, value):
        return queryset.search(value)

class PobladoFilter(django_filters.FilterSet):

    search = django_filters.CharFilter(method='_search')

    class Meta:
        model = models.Poblado
        fields = ['search']
    
    def _search(self, queryset, name, value):
        return queryset.search(value)
