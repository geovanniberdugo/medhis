from promise import Promise
from collections import defaultdict
from django.db.models import Prefetch
from promise.dataloader import DataLoader
from ..models import Plan, Servicio, Tarifa

# Plan

class NombreCompletoByPlan(DataLoader):

    def batch_load_fn(self, ids_plan):
        qs = Plan.objects.select_related('cliente').filter(id__in=ids_plan)
        planes = {plan.id: str(plan) for plan in qs}

        return Promise.resolve([
            planes.get(plan_id, '') for plan_id in ids_plan
        ])

class ClienteByPlan(DataLoader):

    cache = False

    def batch_load_fn(self, ids_plan):
        qs = Plan.objects.select_related('cliente').filter(id__in=ids_plan)
        planes = {plan.id: plan.cliente for plan in qs}

        return Promise.resolve([
            planes.get(plan_id, '') for plan_id in ids_plan
        ])

# Servicio

class TarifasByServicio(DataLoader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plan = None
        self.institucion = None

    def batch_load_fn(self, ids_servicio):
        qs = Servicio.objects.prefetch_related(*self.prefetch()).filter(id__in=ids_servicio)
        servicios = {servicio.id: servicio._tarifas for servicio in qs}

        return Promise.resolve([
            servicios.get(servicio_id, []) for servicio_id in ids_servicio
        ])
    
    def prefetch(self):
        if self.plan or self.institucion:
            _filters = {}
            if self.plan:
                _filters.update({'plan': self.plan})
            if self.institucion:
                _filters.update({'institucion': self.institucion})

            return [Prefetch('tarifas', queryset=Tarifa.objects.filter(**_filters), to_attr='_tarifas')]

        return [Prefetch('tarifas', to_attr='_tarifas')]
