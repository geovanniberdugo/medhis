from contextlib import suppress
from sequences import get_next_value
from sequences.models import Sequence
from django.db import transaction, connection

def consecutivo_factura(institucion):
    """Devuelve el valor del consecutivo para la nueva factura sin actualizar el valor de la secuencia."""

    consecutivo = None
    with suppress(ValueError):
        with transaction.atomic():
            consecutivo = get_next_value(institucion.consecutivo_factura())
            raise ValueError('para que no se actualize la secuencia')

    return consecutivo

def update_consecutivo_factura(institucion, valor):
    """Actualiza la secuencia de la factura."""

    sequence, created = (
        Sequence.objects
            .select_for_update()
            .get_or_create(name=institucion.consecutivo_factura(), defaults={'last': valor})
    )

    if not created:
        sequence.last = valor
        sequence.save()