from datetime import date
from agenda.models import Cita

def anular_factura(factura, razon_anulacion, empleado):

    factura.anulado_por = empleado
    factura.anulado_el = date.today()
    factura.razon_anulacion = razon_anulacion
    factura.save()

    for detalle in factura.detalle.all():
        detalle.citas_anuladas = list(detalle.citas.values_list('id', flat=True))
        detalle.save()

    Cita.objects.facturas([factura]).update(detalle_factura=None)

    return factura
