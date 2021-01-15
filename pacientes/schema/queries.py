import graphene
from graphene_django_extras import (DjangoObjectType, DjangoListObjectType, DjangoObjectField, DjangoListObjectField)
from graphene_django_extras.converter import get_choices
from django.urls import reverse
from common.schema.types import LocalCustomDateTime
from organizacional.schema.queries import Empleado
from servicios.schema.queries import Plan, Cliente
from .. import models
from .. import filters


class Paciente(DjangoObjectType):

    can_edit = graphene.Boolean()
    grupo_sanguineo = graphene.String()
    zona = graphene.String(source='zona')
    edad = graphene.String(source='edad')
    procedencia = graphene.String(source='procedencia')
    nombre_completo = graphene.String(source='__str__')
    estado_civil = graphene.String(source='estado_civil')
    grupo_etnico = graphene.String(source='grupo_etnico')
    citas_url = graphene.String(description='URL de citas del paciente')
    pagos_url = graphene.String(description='URL de los pagos del paciente')
    detail_url = graphene.String(description='URL del detalle del paciente')
    parentesco_responsable = graphene.String(source='parentesco_responsable')
    historias_url = graphene.String(description='URL de las historias del paciente')
    tratamientos_url = graphene.String(description='URL de los tratamientos del paciente')
    edit_url = graphene.String(description='URL de edición del paciente', deprecation_reason='Usar detailUrl')

    class Meta:
        model = models.Paciente
        description = 'Una persona que se va a ser atendendida por la IPS'
    
    def resolve_foto(self, info, **kwargs):
        return self.foto.url if self.foto else ''

    def resolve_firma(self, info, **kwargs):
        return self.firma.url if self.firma else ''

    def resolve_grupo_sanguineo(self, info, **kwargs):
        choices = get_choices(self.GRUPOS_SANGUINEOS)
        grupo = list(filter(lambda o: o[1] == self.grupo_sanguineo, choices))
        return grupo[0][0] if len(grupo) > 0 else ''

    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)

    def resolve_edit_url(self, info, **kwargs):
        return self.edit_url(info.context.user)
    
    def resolve_detail_url(self, info, **kwargs):
        return self.detail_url(info.context.user)

    def resolve_citas_url(self, info, **kwargs):
        return self.citas_url(info.context.user)

    def resolve_pagos_url(self, info, **kwargs):
        return self.pagos_url(info.context.user)

    def resolve_tratamientos_url(self, info, **kwargs):
        return self.tratamientos_url(info.context.user)

    def resolve_historias_url(self, info, **kwargs):
        return self.historias_url(info.context.user)

class PacienteList(DjangoListObjectType):

    class Meta:
        model = models.Paciente
        description = 'Lista de pacientes'
        filterset_class = filters.PacienteFilter

class Orden(DjangoObjectType):

    afiliacion_label = graphene.String(source='get_afiliacion_display')
    tipo_usuario_label = graphene.String(source='get_tipo_usuario_display')
    can_edit = graphene.Boolean(description='Indica si se puede editar la orden')
    total_pagado = graphene.Float(source='total_pagado', description='Total pagado por el paciente')

    class Meta:
        model = models.Orden
        description = 'Indica lo se va a realizar un paciente'
    
    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)
    
    def resolve_institucion(self, info, **kwargs):
        return info.context.dataloaders.institucion_by_orden.load(self.id)

    def resolve_plan(self, info, **kwargs):
        return info.context.dataloaders.plan_by_orden.load(self.id)

class ServicioRealizar(DjangoObjectType):

    convenio = graphene.Field(Plan)
    entidad = graphene.Field(Cliente)
    paciente = graphene.Field(Paciente)
    estado_label = graphene.String(source='get_estado_display')
    iva_coopago = graphene.Float(description='Valor del IVA del coopago')
    coopago_bruto = graphene.Float(description='Valor del coopago sin IVA')
    facturas = graphene.List(graphene.NonNull('facturacion.schema.Factura'))
    total_pagado = graphene.Float(description='Valor pagado por el paciente')
    saldo_paciente = graphene.Float(description='Saldo a pagar del paciente')
    orden_url = graphene.String(description='URL de la orden asociada al tratamiento')
    medicos = graphene.List(Empleado, description='Medicos que atendieron el servicio')
    can_edit = graphene.Boolean(description='Indica si se puede editar el tratamiento')
    valor_total = graphene.Float(source='valor_total', description='Valor total del tratamiento')
    coopago_total = graphene.Float(source='coopago_total', description='Valor total del coopago')
    sesiones_faltantes = graphene.Int(description='Número de sesiones que no han sido atendidas')
    can_delete = graphene.Boolean(description='Indica si el usuario puede eliminar el servicio de la orden')
    fecha_inicio_tratamiento = LocalCustomDateTime(description='Fecha en que el paciente inicio el tratamiento')
    can_reagendar_citas = graphene.Boolean(description='Indica si se pueden reagendar citas para el tratamiento')
    can_edit_valor = graphene.Boolean(description='Indica si se puede editar el valor por sesión del tratamiento')
    control_citas_url = graphene.String(source='control_citas_url', description='URL para la impresion del control de citas')
    valor_pagar_medico = graphene.Float(medico=graphene.ID(required=True), description='Valor que se le debe pagar al medico')
    sesiones_atendidas = graphene.Int(medico=graphene.ID(), desde=graphene.Date(), hasta=graphene.Date(), description='Número de sesiones atendidas')
    fecha_fin_tratamiento = graphene.NonNull(LocalCustomDateTime, source='fin_tratamiento', description='Fecha en que el paciente termina el tratamiento.')
    can_verificar_orden_inicio_tratamiento = graphene.Boolean(description='Indica si el usuario tiene permiso de verificar la orden al inicio del tratamiento')
    saldo_sesiones = graphene.Float(description='Saldo de las sesiones atendidas. Este valor indica si el paciente tiene deuda, esta al día o tiene saldo a favor')

    class Meta:
        model = models.ServicioRealizar
        description = 'Indica el servicio que se va a realizar un paciente'

    def resolve_can_delete(self, info, **kwargs):
        return False

    def resolve_can_reagendar_citas(self, info, **kwargs):
        return self.can_reagendar_citas()

    def resolve_can_edit(self, info, **kwargs):
        return self.can_edit(info.context.user)
    
    def resolve_orden_url(self, info, **kwargs):
        return self.orden_url(info.context.user)

    def resolve_can_edit_valor(self, info, **kwargs):
        return self.can_edit_valor(info.context.user)

    def resolve_can_verificar_orden_inicio_tratamiento(self, info, **kwargs):
        return self.can_verificar_inicio_tratamiento(info.context.user)
    
    def resolve_medicos(self, info, **kwargs):
        return info.context.dataloaders.medicos_by_tratamiento.load(self.id)

    def resolve_facturas(self, info, **kwargs):
        return info.context.dataloaders.facturas_by_tratamiento.load(self.id)

    def resolve_convenio(self, info, **kwargs):
        return info.context.dataloaders.convenio_by_tratamiento.load(self.id)

    def resolve_paciente(self, info, **kwargs):
        return info.context.dataloaders.paciente_by_tratamiento.load(self.id)

    def resolve_orden(self, info, **kwargs):
        return info.context.dataloaders.orden_by_tratamiento.load(self.id)
    
    def resolve_servicio(self, info, **kwargs):
        return info.context.dataloaders.servicio_by_tratamiento.load(self.id)

    def resolve_entidad(self, info, **kwargs):
        return info.context.dataloaders.entidad_by_tratamiento.load(self.id)

    def resolve_fecha_inicio_tratamiento(self, info, **kwargs):
        return info.context.dataloaders.fecha_inicio_by_tratamiento.load(self.id)

    def resolve_total_pagado(self, info, **kwargs):
        return info.context.dataloaders.total_pagado_by_tratamiento.load(self.id)

    def resolve_saldo_paciente(self, info, **kwargs):
        return info.context.dataloaders.saldo_paciente_by_tratamiento.load(self.id)

    def resolve_saldo_sesiones(self, info, **kwargs):
        return info.context.dataloaders.saldo_sesiones_by_tratamiento.load(self.id)

    def resolve_sesiones_atendidas(self, info, medico=None, desde=None, hasta=None, **kwargs):
        info.context.dataloaders.cant_citas_atendidas_by_tratamiento.desde = desde
        info.context.dataloaders.cant_citas_atendidas_by_tratamiento.hasta = hasta
        info.context.dataloaders.cant_citas_atendidas_by_tratamiento.medico = medico
        return info.context.dataloaders.cant_citas_atendidas_by_tratamiento.load(self.id)

    def resolve_valor_pagar_medico(self, info, medico, **kwargs):
        info.context.dataloaders.valor_pagar_medico_by_tratamiento.medico = medico
        return info.context.dataloaders.valor_pagar_medico_by_tratamiento.load(self.id)

    def resolve_sesiones_faltantes(self, info, medico=None, **kwargs):
        return info.context.dataloaders.cant_citas_faltantes_by_tratamiento.load(self.id)

    def resolve_iva_coopago(self, info, **kwargs):
        return info.context.dataloaders.iva_coopago_by_tratamiento.load(self.id)

    def resolve_coopago_bruto(self, info, **kwargs):
        return info.context.dataloaders.coopago_bruto_by_tratamiento.load(self.id)

class ServicioPrestadoList(DjangoListObjectType):

    class Meta:
        model = models.ServicioRealizar
        description = 'Lista de servicios prestados'
        filterset_class = filters.TratamientoFilter

class Acompanante(DjangoObjectType):

    parentesco_label = graphene.String(source='get_parentesco_display')

    class Meta:
        model = models.Acompanante
        description = 'Un acompañante es la persona que asiste a la cita con el paciente'

class Query:
    pacientes = DjangoListObjectField(PacienteList, description='Lista de todos los pacientes')
    paciente = DjangoObjectField(Paciente, description='Un solo paciente')
    orden = DjangoObjectField(Orden, description='Una sola orden')
    tratamientos = DjangoListObjectField(ServicioPrestadoList, description='Lista de todos los tratamientos')
    servicios_prestados = DjangoListObjectField(ServicioPrestadoList, description='Lista de todos los servicios prestados', deprecation_reason='Usar tratamientos')
