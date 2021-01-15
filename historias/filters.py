import django_filters
from pacientes.models import Paciente, ServicioRealizar
from . import models


class FormatoFilter(django_filters.FilterSet):

    class Meta:
        model = models.Formato
        fields = ['id', 'activo']
    
    @property
    def qs(self):
        query = super().qs
        user = getattr(self.request, 'user', None)
        if user:
            return query.by_user(user)
        
        return query


class HistoriaFilter(django_filters.FilterSet):

    tratamiento = django_filters.ModelChoiceFilter(field_name='cita__servicio_prestado', queryset=ServicioRealizar.objects.all())
    paciente = django_filters.ModelChoiceFilter(field_name='cita__servicio_prestado__orden__paciente', queryset=Paciente.objects.all())

    class Meta:
        model = models.Historia
        fields = ['paciente', 'terminada', 'tratamiento', 'formato', 'proveedor']
