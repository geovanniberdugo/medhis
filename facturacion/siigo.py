import io
import calendar
import datetime
import pyexcelerate
from datetime import date
from decimal import Decimal
from servicios.models import Tipo
from pacientes.models import Paciente

# ARL 1305550405
# EPS 1305550401
# OTRA 1305550411
# PART 1305550408
# PRE 1305550404

class Tercero:

    def __init__(self, nombre, email, direccion, telefono, tipo_identificacion, nit, tipo_nit, tipo_persona, sexo, cod_ciudad, es_razon_social, cod_clasificacion_tributaria=7, primer_nombre='', segundo_nombre='', primer_apellido='', segundo_apellido='', actividad_econimica='0010', agente_retenedor='', autoretenedor='', declarante=''):
        self.nit = nit
        self.sexo = sexo
        self.email = email
        self.nombre = nombre
        self.tipo_nit = tipo_nit
        self.telefono = telefono
        self.direccion = direccion
        self.cod_ciudad = cod_ciudad
        self.declarante = declarante
        self.tipo_persona = tipo_persona
        self.autoretenedor = autoretenedor
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.es_razon_social = es_razon_social
        self.segundo_apellido = segundo_apellido
        self.agente_retenedor = agente_retenedor
        self.actividad_economica = actividad_economica
        self.tipo_identificacion = tipo_identificacion
        self.cod_clasificacion_tributaria = cod_clasificacion_tributaria
    
    @staticmethod
    def _format_tipo_id(value):
        if value == Paciente.CEDULA_CIUDADANIA:
            return 'C'
        elif value == Paciente.PASAPORTE:
            return 'P'
        elif value == Paciente.CEDULA_EXTRANJERIA:
            return 'E'
        elif value == Paciente.TARJETA_IDENTIDAD:
            return 'T'
        
        return 'U'

    @classmethod
    def from_paciente(cls, paciente):
        kwargs = { 
            'tipo_nit': 'P',
            'declarante': '',
            'autoretenedor': '',
            'tipo_persona': 1,
            'sexo': paciente.sexo,
            'agente_retenedor': '',
            'es_razon_social': 'N',
            'nombre': str(paciente),
            'email': paciente.email,
            'actividad_economica': '0010',
            'direccion': paciente.direccion,
            'nit': paciente.numero_documento,
            'cod_clasificacion_tributaria': 7,
            'primer_nombre': paciente.primer_nombre,
            'segundo_nombre': paciente.segundo_nombre,
            'primer_apellido': paciente.primer_apellido,
            'segundo_apellido': paciente.segundo_apellido,
            'cod_ciudad': paciente.lugar_residencia.codigo,
            'telefono': paciente.telefono or paciente.celular,
            'tipo_identificacion': cls._format_tipo_id(paciente.tipo_documento),
        }

        return cls(**kwargs)
    
    @classmethod
    def from_cliente(cls, cliente):
        kwargs = {
            'sexo': 'E',
            'email': '',  # TODO guardar email de cliente para facturacion,
            'tipo_nit': 'C',
            'cod_ciudad': 1,
            'tipo_persona': 2,
            'nit': cliente.nit,
            'primer_nombre': '',
            'segundo_nombre': '',
            'primer_apellido': '',
            'segundo_apellido': '',
            'es_razon_social': 'S',
            'declarante': '',  # TODO,
            'autoretenedor': '', # TODO,
            'agente_retenedor': '', # TODO,
            'nombre': cliente.nombre,
            'tipo_identificacion': 'N',
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'cod_clasificacion_tributaria': '',  # TODO cod clasificacion tributaria,
            'actividad_economica': '',  # TODO actividad economica,
        }

        return cls(**kwargs)

    @property
    def digito_verificacion(self):
        return '' # TODO calcular

class Movimiento:

    def __init__(self, tipo, codigo, numero, secuencia, nit, cuenta_contable, fecha, descripcion_movimiento, tipo_transaccion, valor_movimiento, codigo_bodega=0, linea_producto='', codigo_producto='', fecha_cruce='', tipo_cruce='', num_cruce=0, num_vencimiento=0, sucursal=0, codigo_vendedor=1, ciudad=1, zona=1, centro_costos=0, cantidad=0, valor_unitario=0):
        self.nit = nit
        self.tipo = tipo
        self.zona = zona
        self.fecha = fecha
        self.codigo = codigo
        self.numero = numero
        self.ciudad = ciudad
        self.cantidad = cantidad
        self.sucursal = sucursal
        self.num_cruce = num_cruce
        self.secuencia = secuencia
        self.tipo_cruce = tipo_cruce
        self.fecha_cruce = fecha_cruce
        self.codigo_bodega = codigo_bodega
        self.centro_costos = centro_costos
        self.valor_unitario = valor_unitario
        self.linea_producto = linea_producto
        self.num_vencimiento = num_vencimiento
        self.codigo_producto = codigo_producto
        self.cuenta_contable = cuenta_contable
        self.codigo_vendedor = codigo_vendedor
        self.valor_movimiento = valor_movimiento
        self.tipo_transaccion = tipo_transaccion
        self.descripcion_movimiento = descripcion_movimiento

    def serialize(self):
        return [
            self.tipo,
            self.codigo,
            self.numero,
            self.cuenta_contable,
            self.tipo_transaccion,
            self.valor_movimiento,
            self.fecha.year,
            self.fecha.month,
            self.fecha.day,
            self.codigo_vendedor,
            self.ciudad,
            self.zona,
            self.secuencia,
            self.centro_costos,
            0,  # subcentro de costos
            self.nit,
            self.sucursal,
            self.descripcion_movimiento,
            0,  # numero de cheque
            'N',  # comprobante anulado
            0,  # codigo del motivo de devolucion
            0,  # forma de pago
            0,  # valor cargo 1 secuencia
            0,  # valor cargo 2 secuencia
            0,  # valor descuento 1 secuencia
            0,  # valor descuento 2 secuencia
            0,  # % de iva
            0,  # valor de iva
            '',  # base de retencion
            0,  # base reteiva
            'N',  # secuencia gravada o excenta
            '',  # % AIU
            '',  # base iva AIU
            self.linea_producto,  # linea producto
            self.codigo_producto,  # grupo producto
            self.codigo_producto,  # codigo producto
            self.cantidad,  # cantidad
            0,  # cantidad dos
            self.codigo_bodega,
            0,  # codigo de la ubicacion
            self.valor_unitario,  # cant factor de conversion
            0,  # operador de factor de conversion
            0,  # valor de factor de conversion
            '', # tipo documento pedido
            0, # cod comprobante pedido
            0, # num comprobante pedido
            0, # secuencia pedido
            self.tipo_cruce,  # tipo comprobante de cruce
            self.num_cruce,  # numero comprobante de cruce
            self.num_vencimiento,  # numero vencimiento
            getattr(self.fecha_cruce, 'year', ''),
            getattr(self.fecha_cruce, 'month', ''),
            getattr(self.fecha_cruce, 'day', ''),
        ]

class Comprobante:

    def __init__(self, movimientos=[]):
        self.movimientos = movimientos

    @staticmethod
    def _set_nit(recibo):
        cliente = recibo.cliente
        if cliente.factura_paciente:
            return '22222222'  # TODO cuando es particular
        
        return cliente.nit
    
    @staticmethod
    def _set_codigo(sucursal):
        return sucursal.codigo_contable_recibo
    
    @staticmethod
    def _set_cuenta_credito(recibo):
        # TODO parametrizar cuenta
        if recibo.servicio.tipo == Tipo.OTRO:
            return '4295050401'  # Solicitud de documentos en este caso es el unico en otros

        return '2805050402'
    
    @classmethod
    def from_recibo_caja(cls, recibo, sucursal):
        """Un recibo de caja genera 2 movimientos (debito y credito) mismo valor."""

        kwargs = {
            'tipo': 'N',
            'codigo': cls._set_codigo(sucursal),
            'numero': recibo.numero,
            'valor_movimiento': recibo.valor,
            'fecha': recibo.fecha,
            'codigo_vendedor': 1,
            'ciudad': 1,
            'zona': 1,
            'centro_costos': 1,
            'nit': cls._set_nit(recibo),
            'descripcion_movimiento': recibo.detalle,
        }

        return cls([
            Movimiento(cuenta_contable='1105050402', tipo_transaccion='D', secuencia=1, **kwargs),
            Movimiento(cuenta_contable=cls._set_cuenta_credito(recibo), tipo_transaccion='C', secuencia=2, **kwargs),
        ])

    @classmethod
    def from_factura(cls, factura):
        cliente = factura.cliente
        kwargs = {
            'zona': 0,
            'ciudad': 1,
            'tipo': 'F',
            'codigo': 1,
            'codigo_vendedor': 1,
            'tipo_cruce': 'F-001',
            'numero': factura.numero,
            'fecha': factura.fecha_expedicion,
            'nit': cliente.nit.replace('-', ''),
        }

        descripcion = 'Factura {}'.format(factura.numero)
        next_date = next_month(factura.fecha_expedicion)
        year = next_date.year
        month = next_date.month
        fecha_cruce = date(year, month, calendar.monthrange(year, month)[1])
        
        # Fix temp for facturacion electronica
        cantidad = valor_unitario = 0
        if factura.institucion_id == 1: # Si es UMRI
            detalle = factura.detalle.all()
            cantidad = sum(map(lambda o: o.cantidad, detalle))
            valor_unitario = detalle[0].valor
            kwargs['codigo'] = 3
            kwargs['tipo_cruce'] = 'F-003'

        movimientos = [
            Movimiento(tipo_transaccion='C', valor_movimiento=factura.subtotal(), cuenta_contable=factura.puc_subtotal(), secuencia=2, codigo_bodega=1, linea_producto=factura.codigo_linea(), codigo_producto=factura.codigo_producto(), descripcion_movimiento=str(factura.cuenta_siigo()), cantidad=cantidad, valor_unitario=valor_unitario, **kwargs),
            Movimiento(tipo_transaccion='D', valor_movimiento=factura.total(), cuenta_contable=cliente.puc_facturacion, secuencia=1, num_cruce=factura.numero, num_vencimiento=1, fecha_cruce=fecha_cruce, descripcion_movimiento=descripcion, **kwargs),
        ]

        if factura.total_coopago() > 0:
            movimientos.append(
                Movimiento(tipo_transaccion='D', valor_movimiento=factura.total_coopago(), cuenta_contable='2805050402', secuencia=3, centro_costos=1, descripcion_movimiento='Coopago', **kwargs),
            )

        return cls(movimientos)
    
def next_month(date):
    """return a date one month in advance of 'date'. 
        If the next month has fewer days then the current date's month, this will return an
        early date in the following month."""

    return date + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])
        

def _format_fecha(fecha):
    if fecha:
        return fecha.strftime('%Y%m%d')

    return ''

def _format_number(value, size):
    """Llena con 0s a la izq."""

    return '{:0>{}}'.format(value, size)

def _format_decimal(value, int_size, dec_size):
    rounded_value = value.quantize(Decimal('1.{:0<{}}'.format('', dec_size)))
    int_part, dec_part = str(rounded_value).split('.')
    return '{}{}'.format(_format_number(int_part, int_size), dec_part)

def _format_string(value, size):
    """LLena con espacios a la der."""

    return '{:<{}}'.format(value, size)

def _registro_tercero(tercero):
    return [
        # Archivo 1
        _format_number(tercero.nit, 13),
        _format_number(1, 3),  # sucursal
        tercero.tipo_nit,  # C(cliente), P(proveedor), O(Otros)
        _format_string(tercero.nombre, 60),
        _format_string('', 50),  # contacto
        _format_string(tercero.direccion, 100),
        _format_number(tercero.telefono, 11),
        # Archivo 2
        _format_number('', 11),  # telefono2
        _format_number('', 11),  # telefono3
        _format_number('', 11),  # telefono4
        _format_number('', 11),  # fax
        _format_number('', 6),  # apartado aereo
        _format_string(tercero.email, 100),
        tercero.sexo,  # F/M/E(Empresa)
        # (1 gran contribuyente, 2 empr. Estado, 3 reg comun, 4 reg. Simplificado, 5 reg simplificado no residente en el pais, 6 no residente en el pais, 7 no responsable de iva)
        _format_number(tercero.cod_clasificacion_tributaria, 1),
        tercero.tipo_identificacion,
        _format_number('', 11),  # cupo de credito
        _format_number('', 2),  # lista precios (Del 1 al 12) o 13 son todas las listas 
        _format_number(1, 4),  # cod del vendedor
        _format_number(tercero.cod_ciudad, 4),  # cod ciudad
        _format_number('', 11),  # % descuento
        _format_number('', 3),  # periodo pago
        _format_string('', 30),  # observaciones
        _format_number(1, 3),  # cod pais
        tercero.digito_verificacion,
        _format_number('', 3),  # calificacion
        _format_number(tercero.actividad_economica, 5),
        _format_number('', 4),  # cod forma pago
        _format_number('', 4),  # cod cobrador
        _format_number(tercero.tipo_persona, 2),  # (01 - Natural  02 - Jurídica
        tercero.declarante,  # declarante S/N  hacer
        tercero.agente_retenedor,  # agente retenedor S/N hacer
        tercero.autoretenedor,  # autoretenedor S/N  hacer
        '',  # Beneficio reteiva 60% S/N
        '',  # agente retenedor ICA S/N
        'A',  # estado A activo/I inactivo
        '',  # Ente publico S/N ECUADOR
        _format_number('', 10),  # Cod ente publico ECUADOR
        tercero.es_razon_social,
        _format_string(tercero.primer_nombre, 15),
        _format_string(tercero.segundo_nombre, 15),
        _format_string(tercero.primer_apellido, 15),
        _format_string(tercero.segundo_apellido, 15),
        _format_string('', 20),  # id del extranjero
        _format_string('', 3),  # ruta ECUADOR
        _format_string('', 10),  # registro ECUADOR
        _format_string('', 8),  # fecha vencimiento ECUADOR
        _format_string('', 8),  # fecha cumpleaños
        _format_string('', 1),  # tipo sociedad ECUADOR - (S - Sociedad Privada y Extranjeros sin Cedula, P -  Sociedad Publica, N - Persona Natural)
        _format_string('', 10),  # aut impresa ECUADOR
        _format_string('', 11),  # aut contribuyente ECUADOR
        _format_number('', 2),  # tipo contribuyente PERU (Para Colombia 99) - Sin Documento - 2 posiciones - Numéricas)  (00 - Otros Tipos de Documentos  01 - Documento Nacional de Identidad (DNI)  02 - Carnet de Fuerzas Policiales 03 - Carnet de Fuerzas Armadas  04 - Carnet de Extranjería  06 - Registro Unico de Contribuyentes  07 - Pasaporte
        _format_string('', 50),  # contacto factura
        _format_string('', 90),  # email facturacion
    ]

def _registro_movimiento(movimiento):
    return [
        # Archivo 1
        movimiento.tipo,  # ("F"=Factura de venta, "G"=egreso, "P"=registro de compra, N: Recibo de caja)
        _format_number(movimiento.codigo, 3),
        _format_number(movimiento.numero, 11),
        _format_number(movimiento.secuencia, 5),
        _format_number(movimiento.nit, 13),
        _format_number('', 3),  # sucursal
        _format_number(movimiento.cuenta_contable, 10),
        _format_number('', 13),  # cod producto
        _format_fecha(movimiento.fecha),
        _format_number(movimiento.centro_costos, 4),  # centro costos
        _format_number('', 3),  # subcentro costos
        _format_string(movimiento.descripcion_movimiento, 50),
        movimiento.tipo_transaccion,  # ('D': Debito, 'C': Credito)
        _format_decimal(movimiento.valor_movimiento, 13, 2),
        _format_number('', 15),  # base retencion
        _format_number(movimiento.codigo_vendedor, 4),  # cod vendedor
        _format_number(movimiento.ciudad, 4),  # cod ciudad
        _format_number(movimiento.zona, 3),  # cod zona
        _format_number('', 4),  # cod bodega
        _format_number('', 3),  # cod ubicacion
        _format_number('', 15),  # cantidad
        '',  # Tipo documento cruce
        _format_string('', 3),  # cod comprobante cruce
        _format_number('', 11),  # numero documento cruce
        _format_number('', 3),  # secuencia documento cruce
        _format_number('', 8),  # Fecha vencimiento documento
        _format_number('', 4),  # Cod forma pago
        _format_number('', 2),  # cod banco
    ]

def _registro_recibo(recibo, sucursal):
    comprobante = Comprobante.from_recibo_caja(recibo, sucursal)
    return [''.join(_registro_movimiento(movimiento)) for movimiento in comprobante.movimientos]

def exportar_recibos(recibos, sucursal):
    result = []
    for recibo in recibos:
       result.extend(_registro_recibo(recibo, sucursal))
    
    return '\n'.join(result)

def exportar_terceros(terceros):
    return []

def exportar_facturas(facturas):
    result = []
    for factura in facturas:
        result.extend(_registro_factura(factura))
    
    return result

def _registro_factura(factura):
    comprobante = Comprobante.from_factura(factura)
    return [movimiento.serialize() for movimiento in comprobante.movimientos]

def write_to_excel(data):
    mem_file = io.BytesIO()
    wb = pyexcelerate.Workbook()
    ws = wb.new_sheet('Facturas')
    _set_header(ws)
    _set_body(ws, data)
    wb.save(mem_file)
    return mem_file.getvalue()

def _set_header(ws):
    ws.set_cell_value(1, 1, '')
    ws.range('A1', 'BA1').merge()
    ws.set_cell_value(2, 1, '')
    ws.range('A2', 'BA2').merge()
    ws.set_cell_value(3, 1, '')
    ws.range('A3', 'BA3').merge()
    ws.set_cell_value(4, 1, '')
    ws.range('A4', 'BA4').merge()
    ws.range('A5', 'BA5').value = [[
        'TIPO DE COMPROBANTE (OBLIGATORIO)',
        'CÓDIGO COMPROBANTE  (OBLIGATORIO)',
        'NÚMERO DE DOCUMENTO (OBLIGATORIO)',
        'CUENTA CONTABLE   (OBLIGATORIO)',
        'DÉBITO O CRÉDITO (OBLIGATORIO)',
        'VALOR DE LA SECUENCIA   (OBLIGATORIO)',
        'AÑO DEL DOCUMENTO',
        'MES DEL DOCUMENTO',
        'DÍA DEL DOCUMENTO',
        'CÓDIGO DEL VENDEDOR',
        'CÓDIGO DE LA CIUDAD',
        'CÓDIGO DE LA ZONA',
        'SECUENCIA',
        'CENTRO DE COSTO',
        'SUBCENTRO DE COSTO',
        'NIT',
        'SUCURSAL',
        'DESCRIPCIÓN DE LA SECUENCIA',
        'NÚMERO DE CHEQUE',
        'COMPROBANTE ANULADO',
        'CÓDIGO DEL MOTIVO DE DEVOLUCIÓN',
        'FORMA DE PAGO',
        'VALOR DEL CARGO 1 DE LA SECUENCIA',
        'VALOR DEL CARGO 2 DE LA SECUENCIA',
        'VALOR DEL DESCUENTO 1 DE LA SECUENCIA',
        'VALOR DEL DESCUENTO 2 DE LA SECUENCIA',
        'PORCENTAJE DEL IVA DE LA SECUENCIA',
        'VALOR DE IVA DE LA SECUENCIA',
        'BASE DE RETENCIÓN',
        'BASE PARA CUENTAS MARCADAS COMO RETEIVA',
        'SECUENCIA GRAVADA O EXCENTA',
        'PORCENTAJE AIU',
        'BASE IVA AIU',
        'LÍNEA PRODUCTO',
        'GRUPO PRODUCTO',
        'CÓDIGO PRODUCTO',
        'CANTIDAD',
        'CANTIDAD DOS',
        'CÓDIGO DE LA BODEGA',
        'CÓDIGO DE LA UBICACIÓN',
        'CANTIDAD DE FACTOR DE CONVERSIÓN',
        'OPERADOR DE FACTOR DE CONVERSIÓN',
        'VALOR DEL FACTOR DE CONVERSIÓN',
        'TIPO DOCUMENTO DE PEDIDO',
        'CÓDIGO COMPROBANTE DE PEDIDO',
        'NÚMERO DE COMPROBANTE PEDIDO',
        'SECUENCIA DE PEDIDO',
        'TIPO Y COMPROBANTE CRUCE',
        'NÚMERO DE DOCUMENTO CRUCE',
        'NÚMERO DE VENCIMIENTO',
        'AÑO VENCIMIENTO DE DOCUMENTO CRUCE',
        'MES VENCIMIENTO DE DOCUMENTO CRUCE',
        'DÍA VENCIMIENTO DE DOCUMENTO CRUCE'
    ]]

def _set_body(ws, data):
    number_rows = len(data)
    if number_rows > 0:
        ws.range('A6', 'BA{}'.format(6 + number_rows - 1)).value = data
