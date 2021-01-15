import operator
from functools import reduce
from django.db import models
from django.utils import timezone
from django.db import models, transaction
from django.db.models.functions import Coalesce
from django.utils.module_loading import import_string
from django.db.models import OuterRef, Subquery, Q, When, Case, F, Exists

CITA_PATH = 'agenda.models.Cita'

class PacienteQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Paciente."""

    def by_facturas(self, facturas):
        """Un queryset con los pacientes facturados en las facturas ingresadas."""

        return self.filter(ordenes__servicios_realizar__citas__detalle_factura__factura__in=facturas)
    
    def search(self, term):
        """Filtra los pacientes segun el termino. El termino puede ser el numero de documento 
        o el nombre del paciente.
        """

        search_fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
        words = term.split()

        orm_lookups = ['{}__icontains'.format(search_field) for search_field in search_fields]
        orm_lookups.append('numero_documento__iexact')

        conditions = []
        for word in words:
            queries = [models.Q(**{orm_lookup: word}) for orm_lookup in orm_lookups]
            conditions.append(reduce(operator.or_, queries))
        
        return self.filter(reduce(operator.and_, conditions))

class PacienteManager(models.Manager.from_queryset(PacienteQuerySet)):
    """Manager personalizado para el modelo Paciente."""

    pass

class OrdenManager(models.Manager):
    """Manager personalizado para el modelo Orden."""

    pass

class TratamientoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo ServicioRealizar"""

    def by_sucursal(self, sucursal):
        """Filtra los tratamientos por sucursal."""

        return self.filter(citas__sucursal=sucursal)
    
    def by_medico(self, medico):
        """Filtra los tratamientos por medico."""

        return self.filter(citas__medico=medico).distinct()

    def by_institucion(self, institucion):
        """Filtra los tratamientos por institucion."""

        return self.filter(orden__institucion=institucion).distinct()

    def by_cliente(self, cliente):
        """Filtra los tratamientos por cliente."""

        return self.filter(orden__plan__cliente=cliente).distinct()

    def by_estado(self, estado):
        return self.filter(estado=estado)
    
    def facturados(self):
        Cita = import_string(CITA_PATH)
        citas_facturadas = Cita.objects.filter(servicio_prestado=OuterRef('pk'), detalle_factura__isnull=False)
        return self.annotate(facturado=Exists(citas_facturadas)).filter(facturado=True)
    
    def no_facturados(self):
        Cita = import_string(CITA_PATH)
        citas_facturadas = Cita.objects.filter(servicio_prestado=OuterRef('pk'), detalle_factura__isnull=False)
        return self.annotate(facturado=Exists(citas_facturadas)).filter(facturado=False)

    def facturados_entre(self, desde, hasta):
        """Tratamientos facturados en el rango de fechas ingresado."""

        return self.filter(citas__detalle_factura__factura__fecha_expedicion__date__range=(desde, hasta)).distinct()

    def iniciaron_entre(self, desde, hasta):
        """Retorna los tratamientos que iniciaron en el rango de fechas especificado."""

        Cita = import_string(CITA_PATH)
        inicio = Cita.objects.filter(servicio_prestado=OuterRef('id')).dates('inicio', 'day')[:1]
        return self.annotate(fecha_inicio=Subquery(inicio, output_field=models.DateField())).filter(fecha_inicio__range=(desde, hasta))

    def terminaron_entre(self, desde, hasta):
        """Retorna los tratamientos que terminaron entre el rango de fechas especificado."""

        Cita = import_string(CITA_PATH)
        fin = Cita.objects.atendidas().filter(servicio_prestado=OuterRef('id')).dates('inicio', 'day', order='DESC')[:1]
        return (
            self.terminados()
                .annotate(fecha_fin=Subquery(fin, output_field=models.DateField()))
                .filter(fecha_fin__range=(desde, hasta))
        )

    def citas_entre(self, desde, hasta):
        """Tratamientos con citas en el rango de fechas ingresado."""

        return self.filter(citas__inicio__date__range=(desde, hasta)).distinct()
    
    def recibidos_entre(self, desde, hasta):
        """Tratamientos recibidos en el rango de fechas ingresado."""

        return self.filter(recibido_at__range=(desde, hasta))

    def terminados(self):
        """Es considerado terminado si el estado es cancelado o terminado."""

        return self.filter(estado__in=[self.model.CANCELADO, self.model.TERMINADO])
    
    def no_terminados(self):
        """Retorna los tratamientos no terminados."""

        return self.exclude(estado__in=[self.model.CANCELADO, self.model.TERMINADO])

    def tratamientos_terminados(self):
        """Es considerado terminado si el estado es cancelado o terminado."""

        return self.terminados()
    
    def disponibles_recibir_tratamientos_terminados(self):
        """Retorna los tratamientos terminados que no han sido entregados por los medicos."""

        return self.terminados().exclude(recibido_por__isnull=False)
    
    def disponibles_verificar_tratamientos_terminados(self):
        """Retorna los tratamientos terminados que no han sido verificados."""

        return self.terminados().exclude(verificado_por__isnull=False)
    
    def disponibles_auditar_tratamientos_terminados(self, user):
        """Retorna los tratamientos que no han sido auditados"""

        if not user.has_perm('pacientes.can_verificar_pacientes_terminaron_tratamiento'):
            return self.disponibles_recibir_tratamientos_terminados()

        return self.disponibles_verificar_tratamientos_terminados()
    
    def tratamientos_terminados_recibidos(self):
        """Retorna los tratamientos terminados que ya han sido recibidos."""

        return self.terminados().filter(recibido_por__isnull=False)
    
    def tratamientos_terminados_verificados(self):
        """Retorna los tratamientos que ya han sido verificadas."""

        return self.terminados().filter(verificado_por__isnull=False)
    
    def tratamientos_terminados_auditados(self, user):
        """Retorna los tratamientos terminados que ya se les ha auditado la asistencia."""

        if not user.has_perm('pacientes.can_verificar_pacientes_terminaron_tratamiento'):
            return self.tratamientos_terminados_recibidos()

        return self.tratamientos_terminados_verificados()

    def annotate_total_pagado(self):
        """Annotates el tratamiento con el total que ha pagado el paciente."""

        return self.filter(recibos_caja__anulado_por__isnull=True).annotate(_total_pagado=Coalesce(models.Sum('recibos_caja__valor'), 0))

    def annotate_fecha_inicio(self):
        """Annotates el tratamiento con la fecha de inicio."""

        Cita = import_string(CITA_PATH)
        inicial = Cita.objects.filter(servicio_prestado=OuterRef('pk')).values('inicio')[:1]
        return self.annotate(_fecha_inicio=Subquery(inicial, output_field=models.DateTimeField()))
    
    def annotate_num_citas_atendidas(self, medico=None, desde=None, hasta=None):
        """Annotates el tratamiento con el número de citas atendidas."""

        Cita = import_string(CITA_PATH)
        citas = Cita.objects.filter(servicio_prestado=OuterRef('pk')).atendidas().fecha_entre(desde, hasta).order_by()
        if medico:
            citas = citas.by_medico(medico)
        total_citas = citas.values('servicio_prestado').annotate(total=models.Count('id')).values('total')
        return self.annotate(_num_citas_atendidas=Subquery(total_citas, output_field=models.IntegerField()))

    def annotate_coopago_total(self):
        return self.annotate(_coopago_total=Case(
            When(is_coopago_total=True, then='coopago'),
            default=F('coopago') * F('cantidad'),
            output_field=models.DecimalField()
        ))

    def disponibles_abonar_pago(self):
        return self.annotate_total_pagado().annotate_coopago_total().filter(_coopago_total__gt=F('_total_pagado'))

class ServicioRealizarManager(models.Manager.from_queryset(TratamientoQuerySet)):
    """Manager personalizado para el modelo ServicioRealizar."""

    @transaction.atomic
    def agregar_a_orden(self, orden, cantidad, servicio, coopago, medico, sucursal, fecha, empleado, duracion, autorizacion='', fecha_autorizacion=None, is_coopago_total=False, is_una_cita=False):
        """Permite agregar un servicio a una orden."""

        Cita = import_string(CITA_PATH)
        plan = orden.plan
        valor = getattr(plan.tarifa(servicio, orden.institucion), 'valor', 0)
        servicio_prestado = self.model.objects.create(
            orden=orden,
            valor=valor,
            coopago=coopago,
            cantidad=cantidad,
            servicio=servicio,
            is_una_cita=is_una_cita,
            is_coopago_total=is_coopago_total
        )

        cantidad_citas = 1 if is_una_cita else cantidad
        agendar_multiples_citas = import_string('agenda.services.agendar_multiples_citas')
        citas = agendar_multiples_citas(
            medico=medico,
            duracion=duracion,
            sucursal=sucursal,
            empleado=empleado,
            desde=fecha.date(),
            cantidad=cantidad_citas,
            tratamiento=servicio_prestado,
            hora=timezone.localtime(fecha).timetz(),
        )
        
        if plan.sesiones_autorizacion == 0:
            Cita.objects.autorizacion_automatica(citas[0])
        else:
            if plan.sesiones_autorizacion is not None and plan.sesiones_autorizacion > 0:
                citas = citas[:plan.sesiones_autorizacion]
            
            citas_qs = Cita.objects.filter(id__in=map(lambda o: o.id, citas))
            citas_qs.update(autorizacion=autorizacion, fecha_autorizacion=fecha_autorizacion)
        return servicio_prestado
