import django_filters
from organizacional.models import Empleado, Institucion, Sucursal
from servicios.models import Cliente
from . import models

class PacienteFilter(django_filters.FilterSet):
    """Filtro para los pacientes."""

    search = django_filters.CharFilter(method='search_paciente')

    class Meta:
        model = models.Paciente
        fields = ['numero_documento', 'search']
    
    def search_paciente(self, queryset, name, value):
        return queryset.search(value)

class TratamientoFilter(django_filters.FilterSet):
    """Filtro para los servicio prestados."""

    
    ESTADOS = [estado for estado in models.ServicioRealizar.ESTADOS]
    ESTADOS.append(('FAC', 'FACTURADO'))

    citas_entre = django_filters.CharFilter(method='_citas_entre')
    facturados = django_filters.BooleanFilter(method='_facturados')
    terminados = django_filters.BooleanFilter(method='_terminados')
    iniciaron_entre = django_filters.CharFilter(method='_iniciaron_entre')
    recibidos_entre = django_filters.CharFilter(method='_recibidos_entre')
    estado = django_filters.ChoiceFilter(choices=ESTADOS, method='_estado')
    terminaron_entre = django_filters.CharFilter(method='_terminaron_entre')
    facturados_entre = django_filters.CharFilter(method='_facturados_entre')
    auditoria_final = django_filters.BooleanFilter(method='_auditoria_final')
    disponible_pagar = django_filters.BooleanFilter(method='_disponible_pagar')
    cliente = django_filters.ModelChoiceFilter(queryset=Cliente.objects.all(), method='_cliente')
    documento_paciente = django_filters.CharFilter(field_name='orden__paciente__numero_documento')
    sucursal = django_filters.ModelChoiceFilter(queryset=Sucursal.objects.all(), method='_sucursal')
    medico = django_filters.ModelChoiceFilter(queryset=Empleado.objects.medicos(), method='_medico')
    institucion = django_filters.ModelChoiceFilter(queryset=Institucion.objects.all(), method='_institucion')
    tratamientos_terminados_auditados = django_filters.BooleanFilter(method='_tratamientos_terminados_auditados')
    paciente = django_filters.ModelChoiceFilter(queryset=models.Paciente.objects.all(), field_name='orden__paciente')
    tratamientos_terminados_posibles_auditar = django_filters.BooleanFilter(method='posibles_auditar_tratamiento_terminado')

    class Meta:
        model = models.ServicioRealizar
        fields = [
            'estado',
            'sucursal',
            'terminados',
            'iniciaron_entre',
            'auditoria_final',
            'terminaron_entre',
            'disponible_pagar',
            'documento_paciente',
            'tratamientos_terminados_auditados',
            'tratamientos_terminados_posibles_auditar'
        ]
    
    def _estado(self, queryset, name, value):
        if value and value == 'FAC':
            return queryset.facturados()
        elif value:
            return queryset.by_estado(value)

        return queryset

    def _terminados(self, queryset, name, value):
        if value:
            return queryset.terminados()

        return queryset.no_terminados()
    
    def _facturados(self, queryset, name, value):
        if value:
            return queryset.facturados()

        return queryset.no_facturados()

    def _disponible_pagar(self, queryset, name, value):
        if value:
            return queryset.disponibles_abonar_pago()

        return queryset
    
    def _iniciaron_entre(self, queryset, name, value):
        if value:
            return queryset.iniciaron_entre(*value.split(','))

        return queryset
    
    def _terminaron_entre(self, queryset, name, value):
        if value:
            return queryset.terminaron_entre(*value.split(','))

        return queryset

    def _facturados_entre(self, queryset, name, value):
        if value:
            return queryset.facturados_entre(*value.split(','))

        return queryset

    def _recibidos_entre(self, queryset, name, value):
        if value:
            return queryset.recibidos_entre(*value.split(','))

        return queryset

    def _citas_entre(self, queryset, name, value):
        if value:
            return queryset.citas_entre(*value.split(','))

        return queryset
    
    def _medico(self, queryset, name, value):
        if value:
            return queryset.by_medico(value)

        return queryset

    def _sucursal(self, queryset, name, value):
        if value:
            return queryset.by_sucursal(value)

        return queryset

    def _cliente(self, queryset, name, value):
        if value:
            return queryset.by_cliente(value)

        return queryset

    def _institucion(self, queryset, name, value):
        if value:
            return queryset.by_institucion(value)

        return queryset

    def _auditoria_final(self, queryset, name, value):
        if value:
            return queryset.tratamientos_terminados_verificados()

        return queryset
    
    def posibles_auditar_tratamiento_terminado(self, queryset, name, value):
        if value:
            return queryset.disponibles_auditar_tratamientos_terminados(self.request.user)

        return queryset

    def _tratamientos_terminados_auditados(self, queryset, name, value):
        if value:
            return queryset.tratamientos_terminados_auditados(self.request.user)

        return queryset
