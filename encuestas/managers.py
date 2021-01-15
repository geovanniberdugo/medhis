from django.db import models


class SatisfaccionGlobalQuerySet(models.QuerySet):
    
    def rango_fechas(self, desde, hasta):
        """Un queryset con las encuentas realizadas en el rango de fechas ingresado."""

        return self.filter(fecha__range=(desde, hasta))


class SatisfaccionGlobalManager(models.Manager.from_queryset(SatisfaccionGlobalQuerySet)):
    pass


class EventoAdversoQuerySet(models.QuerySet):

    def rango_fechas(self, desde, hasta):
        """Un queryset con los eventos realizadas en el rango de fechas ingresado."""

        return self.filter(fecha__range=(desde, hasta))


class EventoAdversoManager(models.Manager.from_queryset(EventoAdversoQuerySet)):
    pass
