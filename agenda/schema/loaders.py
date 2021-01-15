from promise import Promise
from collections import defaultdict
from promise.dataloader import DataLoader
from ..models import Cita

# Cita

class EstadoDisplayByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.filter(id__in=ids_citas).annotate_estado()
        citas = {cita.id: cita.estado_display for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class MedicoByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('medico').filter(id__in=ids_citas)
        citas = {cita.id: cita.medico for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class TratamientoByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('servicio_prestado').filter(id__in=ids_citas)
        citas = {cita.id: cita.servicio_prestado for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class SucursalByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('sucursal').filter(id__in=ids_citas)
        citas = {cita.id: cita.sucursal for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class ServicioByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('servicio_prestado__servicio').filter(id__in=ids_citas)
        citas = {cita.id: cita.servicio for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class CanMoveByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.can_move for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, False) for cita_id in ids_citas
        ])

class PacienteByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('servicio_prestado__orden__paciente').filter(id__in=ids_citas)
        citas = {cita.id: cita.paciente for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class ConvenioByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('servicio_prestado__orden__plan').filter(id__in=ids_citas)
        citas = {cita.id: cita.empresa for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class HistorialActualByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.historial_actual for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class CumplidaByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.cumplida for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class TerminadaByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.terminada for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class CanceladaByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.cancelada for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class CanAddEncuentroByCita(DataLoader):

    cache = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.can_add_encuentro(self.user) for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])

class EstadosDisponiblesByCita(DataLoader):
    
    cache = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('estados').filter(id__in=ids_citas)
        citas = {cita.id: cita.estados_disponibles(self.user) for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, []) for cita_id in ids_citas
        ])

class EncuentrosByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.prefetch_related('encuentros').filter(id__in=ids_citas)
        citas = {cita.id: cita.encuentros.all() for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, []) for cita_id in ids_citas
        ])

class DetalleFacturaByCita(DataLoader):

    cache = False

    def batch_load_fn(self, ids_citas):
        qs = Cita.objects.select_related('detalle_factura').filter(id__in=ids_citas)
        citas = {cita.id: cita.detalle_factura for cita in qs}

        return Promise.resolve([
            citas.get(cita_id, '') for cita_id in ids_citas
        ])
