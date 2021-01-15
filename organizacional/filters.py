import django_filters
from . import models


class EmpleadoFilter(django_filters.FilterSet):
    """Filtros para los empleados"""

    medicos = django_filters.BooleanFilter(method='filter_medicos')
    individuales = django_filters.BooleanFilter(method='filter_individuales')
    id = django_filters.ModelChoiceFilter(queryset=models.Empleado.objects.all(), method='filter_id')
    sucursal = django_filters.ModelChoiceFilter(queryset=models.Sucursal.objects.all(), method='filter_sucursal')

    class Meta:
        model = models.Empleado
        fields = ['medicos', 'agenda', 'sucursal', 'instituciones', 'individuales', 'id', 'activo']
    
    def filter_medicos(self, queryset, name, value):
        medicos_query = queryset.medicos()
        if value:
            return medicos_query
        return queryset.exclude(id__in=medicos_query)
    
    def filter_individuales(self, queryset, name, value):
        if value:
            return queryset.filter(agenda__isnull=True)
        return queryset
    
    def filter_sucursal(self, queryset, name, value):
        if value:
            return queryset.by_sucursal(value)
        
        return queryset

    def filter_id(self, queryset, name, value):
        if value:
            return queryset.filter(id=value.id)
        
        return queryset
