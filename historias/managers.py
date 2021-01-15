from django.db import models

class FormatoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Formato."""

    def by_user(self, user):
        """
        Filtra los formatos según los permisos del usuario ingresado.

        :param user: Usuario
        """

        permissions = user.get_all_permissions()
        return self.filter(permiso__in=permissions)


class FormatoManager(models.Manager.from_queryset(FormatoQuerySet)):
    """Manager personalizado para el modelo Formato."""

    pass


class HistoriaQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Historia."""

    def con_diagnostico(self):
        """Un queryset con las historias que incluyen diagnostico."""

        return self.filter(formato__diagnostico=True)


class HistoriaManager(models.Manager.from_queryset(HistoriaQuerySet)):
    """Manager personalizado para el modelo Historia."""

    def create_encounter(self, formato, cita, proveedor, data, terminada=False):
        """Crea un encuentro."""

        encuentro = self.model(
            formato=formato, cita=cita, proveedor=proveedor,
            contenido=formato.contenido, data=data, terminada=terminada
        )
        encuentro.save()
        return encuentro
