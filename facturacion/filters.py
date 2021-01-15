import django_filters
from pacientes.models import Paciente
from servicios.models import Cliente
from . import models


class ReciboCajaFilter(django_filters.FilterSet):
    """Filtro para el recibo de caja."""

    anulados = django_filters.BooleanFilter(method='_anulados')
    sucursal = django_filters.NumberFilter(method='by_sucursal')
    fecha_entre = django_filters.CharFilter(method='_fecha_entre')
    fecha__gte = django_filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha__lte = django_filters.DateFilter(field_name='fecha', lookup_expr='lte')
    documento_paciente = django_filters.CharFilter(method='by_documento_paciente')
    caja = django_filters.ModelChoiceFilter(queryset=models.Caja.objects.all(), method='by_caja')
    paciente = django_filters.ModelChoiceFilter(queryset=Paciente.objects.all(), method='by_paciente')
    cliente = django_filters.ModelChoiceFilter(queryset=Cliente.objects.all(), method='by_cliente')

    class Meta:
        model = models.ReciboCaja
        fields = ['fecha', 'sucursal', 'caja', 'documento_paciente', 'paciente', 'numero']
    
    def by_sucursal(self, queryset, name, value):
        return queryset.by_sucursal(value)
    
    def by_caja(self, queryset, name, value):
        return queryset.by_caja(value)
    
    def by_documento_paciente(self, queryset, name, value):
        if value:
            return queryset.by_documento_paciente(value)
        
        return queryset

    def by_paciente(self, queryset, name, value):
        if value:
            return queryset.by_paciente(value)
        
        return queryset

    def by_cliente(self, queryset, name, value):
        if value:
            return queryset.by_cliente(value)
        
        return queryset
    
    def _fecha_entre(self, queryset, name, value):
        if value:
            return queryset.fecha_entre(*value.split(','))
        return queryset

    def _anulados(self, queryset, name, value):
        if value:
            return queryset.anulados()

        return queryset.no_anulados()

class CajaFilter(django_filters.FilterSet):
    """Filtro para las cajas"""

    recibidas = django_filters.BooleanFilter(method='_recibidas')
    verificadas = django_filters.BooleanFilter(method='_verificadas')

    class Meta:
        model = models.Caja
        fields = ['id']
    
    @property
    def qs(self):
        query = super().qs
        user = getattr(self.request, 'user', None)
        if user:
            return query.by_user(user)

        return query
    
    def _recibidas(self, queryset, name, value):
        if value:
            return queryset.recibidas()

        return queryset.no_recibidas()
    
    def _verificadas(self, queryset, name, value):
        if value:
            return queryset.verificadas()

        return queryset.no_verificadas()

class FacturaFilter(django_filters.FilterSet):

    anuladas = django_filters.BooleanFilter(method='_anuladas')
    expedida_entre = django_filters.CharFilter(method='_expedida_entre')

    class Meta:
        model = models.Factura
        fields = ['cliente', 'institucion', 'paciente', 'numero']
    
    def _expedida_entre(self, queryset, name, value):
        if value:
            return queryset.fecha_expedicion_entre(*value.split(','))
        return queryset
    
    def _anuladas(self, queryset, name, value):
        if value:
            return queryset.anulados()

        return queryset.no_anulados()
