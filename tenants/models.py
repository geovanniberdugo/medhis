from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    """Modelo para guardar la información de los clientes gestionados por la aplicación."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    creado_el = models.DateTimeField(_lazy('creado el'), auto_now_add=True)

    class Meta:
        verbose_name = _lazy('tenant')
        verbose_name_plural = _lazy('tenants')

    def __str__(self):
        return self.nombre
