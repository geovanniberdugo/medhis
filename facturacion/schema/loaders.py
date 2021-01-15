from promise import Promise
from collections import defaultdict
from promise.dataloader import DataLoader
from ..models import ReciboCaja, Factura

class SucusalByReciboCaja(DataLoader):

    def batch_load_fn(self, ids_recibos):
        qs = (
            ReciboCaja.objects
            .select_related('sucursal')
            .filter(id__in=ids_recibos)
        )
        recibos = {recibo.id: recibo.sucursal for recibo in qs}

        return Promise.resolve([
            recibos.get(recibo_id, None) for recibo_id in ids_recibos
        ])

class PacienteByReciboCaja(DataLoader):

    def batch_load_fn(self, ids_recibos):
        qs = (
            ReciboCaja.objects
            .select_related('servicio_prestado__orden__paciente')
            .filter(id__in=ids_recibos)
        )
        recibos = {recibo.id: recibo.paciente for recibo in qs}

        return Promise.resolve([
            recibos.get(recibo_id, None) for recibo_id in ids_recibos
        ])

class TotalByFactura(DataLoader):

    def batch_load_fn(self, ids_facturas):
        qs = (
            Factura.objects
            .prefetch_related('detalle')
            .filter(id__in=ids_facturas)
        )
        facturas = {factura.id: factura.total() for factura in qs}

        return Promise.resolve([
            facturas.get(factura_id, None) for factura_id in ids_facturas
        ])
