from django.utils.module_loading import import_string
from django.db import models


PATH_TIPO = 'servicios.models.Tipo'

class TipoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Tipo."""

    def consultas(self):
        """Un queryset con los tipos que pertenecen a la clase de consultas."""

        return self.filter(clase=self.model.CONSULTA)
    
    def procedimientos(self):
        """Un queryset con los tipos que pertenecen a la clase procedimiento."""

        return self.filter(clase__in=[
            self.model.PROCEDIMIENTO_DIAGNOSTICO,
            self.model.PROCEDIMIENTO_TERAPEUTICO_QUIRURGICO,
            self.model.PROCEDIMIENTO_TERAPEUTICO_NO_QUIRURGICO
        ])
    
    def not_otros(self):
        """"Un queryset con todos los tipos excluyendo los que pertenecen a la clase otro."""

        return self.exclude(clase__in=[self.model.OTRO])
    
    def in_indicadores(self):
        """Un queryset con los tipos de servicios que deben salir en los indicadores."""

        return self.filter(in_indicadores=True)

class TipoManager(models.Manager.from_queryset(TipoQuerySet)):
    """Manager personalizado para el modelo Tipo."""

    pass

class ServicioQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Servicio."""

    def consultas(self):
        """Un queryset con los servicios categorizados como consultas."""
        
        Tipo = import_string(PATH_TIPO)
        return self.filter(tipo__in=Tipo.objects.consultas())
    
    def procedimientos(self):
        """Un queryset con los servicios categorizados como procedimientos."""
        
        Tipo = import_string(PATH_TIPO)
        return self.filter(tipo__in=Tipo.objects.procedimientos())
    
    def not_otros(self):
        """Un queryset con todos servicios que no pertenecen a la clase otro."""

        Tipo = import_string(PATH_TIPO)
        return self.exclude(tipo__in=Tipo.objects.not_otros())
    
    def by_institucion(institucion):
        """Un queryset con los servicios filtrados por institucion."""

        return self.filter(tarifas__institucion=institucion)

class ServicioManager(models.Manager.from_queryset(ServicioQuerySet)):
    """Manager personalizado para el modelo Servicio."""

    pass
