from django.contrib.postgres.search import SearchVector
from django.db import models


class CieQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Cie."""

    def search(self, term):
        """Permite filtrar los codigos por codigo o nombre."""
        
        return self.filter(models.Q(codigo__icontains=term) | models.Q(nombre__icontains=term))


class CieManager(models.Manager.from_queryset(CieQuerySet)):
    """Manager personalizado para el modelo Cie."""

    pass

class PobladoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Poblado."""

    def search(self, term):
        """Permite filtrar los poblados por id o nombre."""

        try:
            return self.filter(id=int(term))
        except:
            return self.filter(nombre__icontains=term)


class PobladoManager(models.Manager.from_queryset(PobladoQuerySet)):
    """Manager personalizado para el modelo Poblado."""

    pass
