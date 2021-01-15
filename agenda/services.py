from django.db import transaction
from datetime import datetime, timedelta, date
from pacientes.models import Paciente, Orden, Tratamiento
from .models import Cita, HistorialEstado
from common import logger
from . import utils

@transaction.atomic
def agendar_cita(paciente_data, estado, empleado, institucion, servicio, convenio, medico, inicio, duracion, sucursal, **kwargs):
    fin = utils.fin_cita(inicio, duracion)
    paciente = _guardar_paciente(paciente_data)
    tratamiento = _crear_orden(institucion, servicio, convenio, paciente)
    cita = Cita.objects.create(servicio_prestado=tratamiento, inicio=inicio, fin=fin, medico=medico, sucursal=sucursal, **kwargs)
    cita.actualizar_estado(estado, empleado)
    if convenio.sesiones_autorizacion == 0:
        Cita.objects.autorizacion_automatica(cita)
    return cita

def _guardar_paciente(data):
        """Crea o actualiza el paciente."""

        documento = data.pop('numero_documento')
        paciente, _ = Paciente.objects.update_or_create(numero_documento=documento, defaults=data)
        return paciente

def _crear_orden(institucion, servicio, convenio, paciente):
        """
        Crea la orden y el servicio prestado para la cita.

        :returns: El servicio asociado a la cita
        """

        tarifa = convenio.tarifa(servicio, institucion)
        coopago = getattr(tarifa, 'coopago', 0)
        valor = getattr(tarifa, 'valor', 0)
        orden = Orden.objects.create(paciente=paciente, plan=convenio, institucion=institucion)
        return Tratamiento.objects.create(orden=orden, servicio=servicio, valor=valor, coopago=coopago)

@transaction.atomic
def agendar_multiples_citas(cantidad, desde, hora, duracion, medico, sucursal, tratamiento, empleado, aut='', fecha_aut=None):

    def fechas_disponibles_agendar(fecha, cantidad):
        fechas = [fecha]
        for _ in range(cantidad):
            fecha += timedelta(days=1)
            fechas.append(fecha)
        disponibles = filter(lambda h: len(h[1]) > 0, medico.horas_atencion(fechas, sucursal).items())
        return fecha + timedelta(days=1), map(lambda x: _get_espacio_correcto(x[0], x[1]), disponibles)
    
    citas = []
    try:
        fechas_disponibles = []
        fecha_actual = datetime.combine(desde, hora)
        while len(fechas_disponibles) < cantidad:
            fecha_actual, disponibles = fechas_disponibles_agendar(fecha_actual, cantidad - len(fechas_disponibles))
            fechas_disponibles.extend(disponibles)

        for i in range(cantidad):
            fecha = fechas_disponibles[i]
            citas.append(Cita(
                inicio=fecha,
                medico=medico,
                sucursal=sucursal,
                fecha_deseada=fecha,
                servicio_prestado=tratamiento,
                fin=utils.fin_cita(fecha, duracion)
            ))
        Cita.objects.bulk_create(citas)

        estados_citas = [
            HistorialEstado(estado=HistorialEstado.NO_CONFIRMADA,empleado=empleado, cita=cita)
            for cita in citas
        ]
        HistorialEstado.objects.bulk_create(estados_citas)

        num_sesiones = tratamiento.orden.plan.sesiones_autorizacion
        if num_sesiones == 0:
            Cita.objects.autorizacion_automatica(citas[0])
        elif num_sesiones is None:
            agregar_autorizacion(citas[0], aut, fecha_aut)
    except Exception as e:
        logger.exception('.......... Error nose ......... cantidad {}. medico {}. sucursal {}. tratamiento {}. citas {}'.format(cantidad, medico, sucursal, tratamiento, citas))
        raise
    return citas

def _get_espacio_correcto(fecha, espacios_disponibles):
        hora = fecha.time()
        if hora in espacios_disponibles:
            return fecha

        diff = list(map(
            lambda e: abs(datetime.combine(date.today(), hora) - datetime.combine(date.today(), e)),
            espacios_disponibles
        ))

        return datetime.combine(fecha.date(), espacios_disponibles[diff.index(min(diff))])


@transaction.atomic
def agregar_autorizacion(cita, autorizacion, fecha_autorizacion, autorizado_por=''):

    citas = Cita.objects.filter(id=cita.id)
    num_sesiones = cita.servicio_prestado.orden.plan.sesiones_autorizacion
    if num_sesiones is None or num_sesiones == 0:
        citas = cita.servicio_prestado.citas.all()

    citas.update(autorizacion=autorizacion, fecha_autorizacion=fecha_autorizacion, autorizado_por=autorizado_por)
