from django.db import models


class UpdateModelMixin:
    """
    Mixin para actualizar campos de un modelo.
    """

    def update(self, **options):
        """
        Actualiza los datos del modelo.

        :param **options:
            Las opciones en clave:valor que van a ser cambiadas de los atributos del modelo.
        """

        keys = []
        for key, value in options.items():
            setattr(self, key, value)
            keys.append(key)
        self.save(update_fields=keys)