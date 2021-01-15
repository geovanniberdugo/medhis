import django_filters
from graphene_django.filter import filterset
from django_filters import rest_framework as filters
from organizacional.models import Sucursal, Empleado, Institucion
from pacientes.models import Paciente
from servicios.models import Plan, Cliente
from . import models


class CitaFilter(django_filters.FilterSet):
    """Filtro para las citas."""

    atendida = django_filters.BooleanFilter(method='atendidas')
    facturada = django_filters.BooleanFilter(method='facturadas')
    fecha_entre = django_filters.CharFilter(method='_fecha_entre')
    no_cumplidas = django_filters.BooleanFilter(method='_no_cumplidas')
    end__lte = django_filters.DateFilter(field_name='fin', lookup_expr='date__lte')
    end__gte = django_filters.DateFilter(field_name='fin', lookup_expr='date__gte')
    auditados_entre = django_filters.CharFilter(method='_auditados_entre')
    start = django_filters.DateFilter(field_name='inicio', lookup_expr='date')
    start__lte = django_filters.DateFilter(field_name='inicio', lookup_expr='date__lte')
    start__gte = django_filters.DateFilter(field_name='inicio', lookup_expr='date__gte')
    disponible_facturar = django_filters.BooleanFilter(method='_disponible_facturar')
    no_asociada_orden = django_filters.BooleanFilter(field_name='servicio_prestado', lookup_expr='isnull')
    agenda = django_filters.ModelChoiceFilter(field_name='medico__agenda', queryset=models.Agenda.objects.all())
    documento_paciente = django_filters.CharFilter(field_name='servicio_prestado__orden__paciente__numero_documento')
    empresa = django_filters.ModelChoiceFilter(field_name='servicio_prestado__orden__plan__cliente', queryset=Cliente.objects.all())
    paciente = django_filters.ModelChoiceFilter(field_name='servicio_prestado__orden__paciente', queryset=Paciente.objects.all())
    institucion = django_filters.ModelChoiceFilter(field_name='servicio_prestado__orden__institucion', queryset=Institucion.objects.all())

    class Meta:
        model = models.Cita
        fields = ['sucursal', 'empresa', 'medico']
    
    @property
    def qs(self):
        query = super().qs
        user = getattr(self.request, 'user', None)
        if user:
            return query.by_user(user)

        return query
    
    def atendidas(self, queryset, name, value):
        if value:
            return queryset.atendidas()
        
        return queryset.no_atendidas()

    def facturadas(self, queryset, name, value):
        if value:
            return queryset.facturadas()
        
        return queryset.no_facturadas()
    
    def _no_cumplidas(self, queryset, name, value):
        if value:
            return queryset.no_cumplidas()

        return queryset
    
    def _disponible_facturar(self, queryset, name, value):
        if value:
            return queryset.disponibles_facturar()
        
        return queryset

    def _auditados_entre(self, queryset, name, value):
        if value:
            return queryset.auditados_fin_tratamiento_entre(*value.split(','))
        return queryset

    def _fecha_entre(self, queryset, name, value):
        if value:
            return queryset.fecha_entre(*value.split(','))
        return queryset

