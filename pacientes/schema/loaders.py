from promise import Promise
from collections import defaultdict
from promise.dataloader import DataLoader
from ..models import ServicioRealizar, Orden
from organizacional.models import Empleado
from agenda.models import Cita

# Orden

class PlanByOrden(DataLoader):

    cache = False

    def batch_load_fn(self, ids_orden):
        qs = Orden.objects.select_related('plan').filter(id__in=ids_orden)
        ordenes = {orden.id: orden.plan for orden in qs}

        return Promise.resolve([
            ordenes.get(orden_id, None) for orden_id in ids_orden
        ])

class institucionByOrden(DataLoader):

    cache = False

    def batch_load_fn(self, ids_orden):
        qs = (
            Orden.objects
            .select_related('institucion')
            .filter(id__in=ids_orden)
        )
        ordenes = {
            orden.id: orden.institucion for orden in qs}

        return Promise.resolve([
            ordenes.get(orden_id, None) for orden_id in ids_orden
        ])

# Tratamiento
class OrdenByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        qs = (
            ServicioRealizar.objects
            .select_related('orden')
            .filter(id__in=ids_tratamientos)
        )
        tratamientos = {tratamiento.id: tratamiento.orden for tratamiento in qs}

        return Promise.resolve([
            tratamientos.get(tratamiento_id, None) for tratamiento_id in ids_tratamientos
        ])

class FacturasByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        facturas = defaultdict(list)

        for cita in Cita.objects.select_related('detalle_factura__factura').filter(servicio_prestado__in=ids_tratamientos):
            if cita.factura:
                facturas[cita.servicio_prestado_id].append(cita.factura)

        return Promise.resolve([
            set(facturas.get(tratamiento_id, [])) for tratamiento_id in ids_tratamientos
        ])

class MedicosByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        medicos = defaultdict(list)

        for cita in Cita.objects.select_related('medico').filter(servicio_prestado__in=ids_tratamientos):
            medicos[cita.servicio_prestado_id].append(cita.medico)
        
        return Promise.resolve([
            set(medicos.get(tratamiento_id, [])) for tratamiento_id in ids_tratamientos
        ])

class ConvenioByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        qs = ServicioRealizar.objects.select_related('orden__plan').filter(id__in=ids_tratamientos)
        convenios = {tratamiento.id: tratamiento.convenio for tratamiento in qs}

        return Promise.resolve([
            convenios.get(tratamiento, None) for tratamiento in ids_tratamientos
        ])

class PacienteByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.select_related('orden__paciente').filter(id__in=tratamientos)
        pacientes = {tratamiento.id: tratamiento.paciente for tratamiento in qs}

        return Promise.resolve([
            pacientes.get(tratamiento, None) for tratamiento in tratamientos
        ])

class EntidadByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.select_related('orden__plan__cliente').filter(id__in=tratamientos)
        entidades = {tratamiento.id: tratamiento.entidad for tratamiento in qs}

        return Promise.resolve([
            entidades.get(tratamiento, None) for tratamiento in tratamientos
        ])

class ServicioByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        qs = ServicioRealizar.objects.select_related('servicio').filter(id__in=ids_tratamientos)
        servicios = {tratamiento.id: tratamiento.servicio for tratamiento in qs}

        return Promise.resolve([
            servicios.get(id, None) for id in ids_tratamientos
        ])

class FechaInicioByTratamiento(DataLoader):

    cache = False
    
    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.filter(id__in=tratamientos).annotate_fecha_inicio()
        fechas = {tratamiento.id: tratamiento.inicio_tratamiento for tratamiento in qs}

        return Promise.resolve([
            fechas.get(tratamiento, None) for tratamiento in tratamientos
        ])

class TotalPagadoByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.filter(id__in=tratamientos).annotate_total_pagado()
        totales = {tratamiento.id: tratamiento.total_pagado for tratamiento in qs}
        
        return Promise.resolve([
            totales.get(tratamiento, 0) for tratamiento in tratamientos
        ])

class SaldoPacienteByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.filter(id__in=tratamientos).annotate_total_pagado()
        totales = {tratamiento.id: tratamiento.saldo_paciente for tratamiento in qs}
        
        return Promise.resolve([
            totales.get(tratamiento, 0) for tratamiento in tratamientos
        ])

class SaldoSesionesByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, ids_tratamientos):
        qs = (
            ServicioRealizar.objects
                .filter(id__in=ids_tratamientos)
                .annotate_num_citas_atendidas()
                .annotate_total_pagado()
        )
        totales = {tratamiento.id: tratamiento.saldo_sesiones for tratamiento in qs}
        
        return Promise.resolve([
            totales.get(tratamiento, 0) for tratamiento in ids_tratamientos
        ])

class CantCitasAtendidasByTratamiento(DataLoader):

    cache = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.medico = None
        self.desde = None
        self.hasta = None
    
    def batch_load_fn(self, ids_tratamientos):
        qs = (
            ServicioRealizar.objects
                .filter(id__in=ids_tratamientos)
                .annotate_num_citas_atendidas(self.medico, self.desde, self.hasta)
        )
        totales = {tratamiento.id: tratamiento.numero_sesiones_atendidas(self.medico) for tratamiento in qs}

        return Promise.resolve([
            totales.get(tratamiento_id, 0) for tratamiento_id in ids_tratamientos
        ])

class ValorPagarMedicoByTratamiento(DataLoader):

    cache = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.medico = None
    
    def batch_load_fn(self, ids_tratamientos):
        medico = Empleado.objects.get(id=self.medico)
        qs = ServicioRealizar.objects.filter(id__in=ids_tratamientos)
        totales = {tratamiento.id: tratamiento.valor_pagar_medico(medico) for tratamiento in qs}

        return Promise.resolve([
            totales.get(tratamiento_id, 0) for tratamiento_id in ids_tratamientos
        ])

class CantCitasFaltantesByTratamiento(DataLoader):

    cache = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def batch_load_fn(self, tratamientos):
        qs = ServicioRealizar.objects.filter(id__in=tratamientos).annotate_num_citas_atendidas()
        totales = {tratamiento.id: tratamiento.numero_sesiones_faltantes for tratamiento in qs}

        return Promise.resolve([
            totales.get(tratamiento, 0) for tratamiento in tratamientos
        ])

class IvaCoopagoByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamiento_ids):
        qs = (
            ServicioRealizar.objects
            .filter(id__in=tratamiento_ids)
            .select_related('orden__institucion', 'orden__plan', 'orden__plan__cliente')
            .prefetch_related('servicio__tarifas')
        )
        tratamientos = {tratamiento.id: tratamiento.iva_coopago for tratamiento in qs}

        return Promise.resolve([
            tratamientos.get(tratamiento_id, None) for tratamiento_id in tratamiento_ids
        ])

class CoopagoBrutoByTratamiento(DataLoader):

    cache = False

    def batch_load_fn(self, tratamiento_ids):
        qs = (
            ServicioRealizar.objects
            .filter(id__in=tratamiento_ids)
            .select_related('orden__institucion', 'orden__plan', 'orden__plan__cliente')
            .prefetch_related('servicio__tarifas')
        )
        tratamientos = {tratamiento.id: tratamiento.coopago_bruto for tratamiento in qs}

        return Promise.resolve([
            tratamientos.get(tratamiento_id, None) for tratamiento_id in tratamiento_ids
        ])
