from promise import Promise
from promise.dataloader import DataLoader
from ..models import Historia
from common import logger
from .. import utils

class PrintContentByHistoria(DataLoader):

    cache = False

    def batch_load_fn(self, ids_historias):
        qs = Historia.objects.select_related('cita__servicio_prestado__servicio__tipo', 'formato').filter(id__in=ids_historias)
        historias = {historia.id: utils.flatten_medical_record(historia.contenido, historia.data, historia.formato.diagnostico, historia.cita.servicio) for historia in qs}

        return Promise.resolve([
            historias.get(historia_id, '') for historia_id in ids_historias
        ])

class ProveedorByHistoria(DataLoader):

    cache = False

    def batch_load_fn(self, ids_historias):
        qs = Historia.objects.select_related('proveedor').filter(id__in=ids_historias)
        historias = {historia.id: historia.proveedor for historia in qs}

        return Promise.resolve([
            historias.get(historia_id, '') for historia_id in ids_historias
        ])

class FormatoByHistoria(DataLoader):

    cache = False

    def batch_load_fn(self, ids_historias):
        qs = Historia.objects.select_related('formato').filter(id__in=ids_historias)
        historias = {historia.id: historia.formato for historia in qs}

        return Promise.resolve([
            historias.get(historia_id, '') for historia_id in ids_historias
        ])
