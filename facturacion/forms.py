from datetime import date
from decimal import Decimal
from django import forms
from agenda.models import Cita
from servicios.models import Cliente
from pacientes.models import Paciente, Orden
from organizacional.models import Institucion, Sucursal
from .models import Factura, ReciboCaja
from .siigo import exportar_recibos, exportar_terceros, exportar_facturas

class FacturacionSiigoForm(forms.Form):
    desde = forms.DateField()
    hasta = forms.DateField()
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def exportar_facturas(self):
        facturas = (
            Factura.objects
                .no_anulados()
                .cliente(self.cleaned_data['cliente'])
                .institucion(self.cleaned_data['institucion'])
                .fecha_expedicion_entre(self.cleaned_data['desde'], self.cleaned_data['hasta'])
                .prefetch_related('detalle__citas__servicio_prestado__servicio__tipo', 'cliente')
        )
        return exportar_facturas(facturas)

class RipsForm(forms.Form):

    CONTROL = 'CT'
    USUARIOS = 'US'
    CONSULTA = 'AC'
    URGENCIAS = 'AU'
    TRANSACCIONES = 'AF'
    RECIEN_NACIDOS = 'AN'
    PROCEDIMIENTOS = 'AP'
    HOSPITALIZACION = 'AH'
    DESCRIPCION_AGRUPADA = 'AD'
    TIPOS = (
        (CONTROL, CONTROL),
        (USUARIOS, USUARIOS),
        (CONSULTA, CONSULTA),
        (URGENCIAS, URGENCIAS),
        (TRANSACCIONES, TRANSACCIONES),
        (RECIEN_NACIDOS, RECIEN_NACIDOS),
        (PROCEDIMIENTOS, PROCEDIMIENTOS),
        (HOSPITALIZACION, HOSPITALIZACION),
        (DESCRIPCION_AGRUPADA, DESCRIPCION_AGRUPADA),
    )
    
    desde = forms.DateField()
    hasta = forms.DateField()
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def _formato_fecha(self, fecha):
        if fecha:
            return fecha.strftime('%d/%m/%Y')

        return ''
    
    def _get_edad(self, edad):
        return edad.split()[0]
    
    def _get_unidad_edad(self, edad):
        unidad = edad.split()[1]

        if unidad == 'Años':
            return 1
        elif unidad == 'Meses':
            return 2
        else:
            return 3

    def _format_tipo_usuario(self, tipo):
        if tipo == Orden.CONTRIBUTIVO:
            return 1
        elif tipo == Orden.SUBSIDIADO:
            return 2
        elif tipo == Orden.VINCULADO:
            return 3
        elif tipo == Orden.PARTICULAR:
            return 4
        else:
            return 5

    def _format_diagnostico(self, diagnostico):
        if diagnostico:
            return diagnostico['codigo']
        
        return ''
    
    def _format_money(self, value):
        return str(value.quantize(Decimal('0.00')))

    def _registro_transaccion(self, factura):
        cliente = factura.cliente
        institucion = factura.institucion

        return ','.join([
            institucion.codigo,
            institucion.razon_social,
            institucion.tipo_documento,
            institucion.identificacion.replace('-', ''),
            str(factura.numero),
            self._formato_fecha(factura.fecha_expedicion),
            self._formato_fecha(factura.fecha_inicio or factura.fecha_expedicion),
            self._formato_fecha(factura.fecha_fin or factura.fecha_expedicion  ),
            cliente.codigo,
            cliente.razon_social,
            '',  # TODO numero contrato entre cliente
            '',  # TODO plan de beneficios
            '',  # TODO numero de poliza
            self._format_money(factura.total_coopago()),
            self._format_money(Decimal(0)),  # valor de la comision
            self._format_money(Decimal(0)),  # valor de descuento
            self._format_money(factura.total())
        ])

    def _archivo_transacciones(self, facturas):
        return map(lambda o: self._registro_transaccion(o), facturas)
    
    def _registro_descripcion_agrupada(self, cita, institucion):
        factura = cita['factura']
        return ','.join([
            str(factura.numero),
            institucion.codigo,
            cita['clase'],
            str(cita['cantidad']),
            self._format_money(Decimal(0)),  # valor unitario
            self._format_money(cita['total'])
        ])
    
    def _filtro_citas_descripcion(self, citas):
        citas_agrupadas = {}
        for cita in citas:
            factura = cita.factura
            clase = cita.servicio.clase
            key = '{}-{}'.format(factura.id, clase)
            if key in citas_agrupadas:
                citas_agrupadas[key]['cantidad'] = citas_agrupadas[key]['cantidad'] + 1
                citas_agrupadas[key]['total'] = citas_agrupadas[key]['total'] + cita.servicio_prestado.valor
            else:
                citas_agrupadas[key] = {'factura': factura, 'clase': clase, 'cantidad': 1, 'total': cita.servicio_prestado.valor}
        
        return map(lambda key: citas_agrupadas[key], citas_agrupadas.keys())

    def _archivo_descripcion_agrupada(self, facturas, institucion):
        citas = self._filtro_citas_descripcion((
            Cita.objects
                .not_otros()
                .facturas(facturas)
                .select_related('detalle_factura__factura', 'servicio_prestado__servicio__tipo')
        ))
        return map(lambda cita: self._registro_descripcion_agrupada(cita, institucion), citas)

    def _registro_usuario(self, paciente, cliente):
        return ','.join([
            paciente.tipo_documento,
            paciente.numero_documento,
            cliente.codigo,
            str(self._format_tipo_usuario(paciente.tipo_usuario)),
            paciente.primer_apellido,
            paciente.segundo_apellido,
            paciente.primer_nombre,
            paciente.segundo_nombre,
            self._get_edad(paciente.edad),  # TODO edad (numero hasta la fecha del servicio)
            str(self._get_unidad_edad(paciente.edad)),
            paciente.genero,
            paciente.lugar_residencia.municipio.departamento.codigo,
            paciente.lugar_residencia.municipio.codigo,
            paciente.zona
        ])
    
    def _archivo_usuarios(self, facturas, cliente):
        pacientes = (
            Paciente.objects
                .by_facturas(facturas)
                .select_related('lugar_residencia__municipio__departamento')
                .distinct()
        )
        return map(lambda o: self._registro_usuario(o, cliente), pacientes)

    def _registro_consulta(self, institucion, cita):
        paciente = cita.paciente
        factura = cita.factura

        return ','.join([
            str(factura.numero),
            institucion.codigo,
            paciente.tipo_documento,
            paciente.numero_documento,
            self._formato_fecha(cita.inicio),
            cita.autorizacion,
            cita.servicio.cups,
            cita.diagnostico['finalidad'],
            cita.diagnostico['causaExterna'],
            self._format_diagnostico(cita.diagnostico['diagnosticoPrincipalItem']),
            self._format_diagnostico(cita.diagnostico.get('diagnostico1Item', None)),
            self._format_diagnostico(cita.diagnostico.get('diagnostico2Item', None)),
            self._format_diagnostico(cita.diagnostico.get('diagnostico3Item', None)),
            str(cita.diagnostico['tipoDiagnostico']),
            self._format_money(cita.servicio_prestado.valor),
            self._format_money(cita.servicio_prestado.coopago),
            self._format_money(cita.servicio_prestado.valor_pagar)
        ])
    
    def _archivo_consultas(self, facturas, institucion):
        citas = (
            Cita.objects
                .consultas()
                .facturas(facturas)
                .prefetch_related('encuentros__formato')
                .select_related('detalle_factura__factura', 'servicio_prestado__orden__paciente', 'servicio_prestado__servicio')
        )
        return map(lambda cita: self._registro_consulta(institucion, cita), citas)
    
    def _registro_procedimiento(self, institucion, cita):
        paciente = cita.paciente
        factura = cita.factura

        return ','.join([
            str(factura.numero),
            institucion.codigo,
            paciente.tipo_documento,
            paciente.numero_documento,
            self._formato_fecha(cita.inicio),
            cita.autorizacion,
            cita.servicio.cups,
            cita.diagnostico['ambito'],
            cita.diagnostico['finalidad'],
            cita.diagnostico['personalAtiende'],
            self._format_diagnostico(cita.diagnostico.get('diagnosticoPrincipalItem', None)),
            self._format_diagnostico(cita.diagnostico.get('diagnosticoRelacionadoItem', None)),
            self._format_diagnostico(cita.diagnostico.get('complicacionItem', None)),
            cita.diagnostico['formaActoQuirurgico'],
            self._format_money(cita.servicio_prestado.valor_pagar)
        ])
    
    def _archivo_procedimientos(self, facturas, institucion):
        # TODO revisar si se debe agrupar por autorizacion
        citas = (
            Cita.objects
                .procedimientos()
                .facturas(facturas)
                .prefetch_related('encuentros__formato')
                .select_related('detalle_factura__factura', 'servicio_prestado__orden__paciente', 'servicio_prestado__servicio')
        )
        return map(lambda cita: self._registro_procedimiento(institucion, cita), citas)

    def _registro_control(self, institucion, fecha, nombre_archivo, cantidad):
        return ','.join([
            institucion.codigo,
            self._formato_fecha(fecha),
            nombre_archivo[:-4],
            str(cantidad)
        ])
    
    def _nombre_archivo(self, tipo):
        today = date.today()
        return '{}{}.txt'.format(tipo, today.strftime('%m%Y'))

    def _rip_file(self, tipo, facturas, institucion, cliente):
        if tipo == self.TRANSACCIONES:
            registros = self._archivo_transacciones(facturas)
        elif tipo == self.DESCRIPCION_AGRUPADA:
            registros = self._archivo_descripcion_agrupada(facturas, institucion)
        elif tipo == self.USUARIOS:
            registros = self._archivo_usuarios(facturas, cliente)
        elif tipo == self.CONSULTA:
            registros = self._archivo_consultas(facturas, institucion)
        elif tipo == self.PROCEDIMIENTOS:
            registros = self._archivo_procedimientos(facturas, institucion)
            
        return registros

    def generar_rips(self):
        desde = self.cleaned_data['desde']
        hasta = self.cleaned_data['hasta']
        cliente = self.cleaned_data['cliente']
        institucion = self.cleaned_data['institucion']
        fecha_remision = date.today()

        files = []
        control = []
        facturas = self._facturas_periodo(desde, hasta, cliente, institucion)
        # rip_files = [self.TRANSACCIONES, self.DESCRIPCION_AGRUPADA, self.USUARIOS, self.CONSULTA, self.PROCEDIMIENTOS]
        rip_files = [self.TRANSACCIONES, self.USUARIOS, self.CONSULTA, self.PROCEDIMIENTOS]
        for rip_file in rip_files:
            data = list(self._rip_file(rip_file, facturas, institucion, cliente))
            nombre = self._nombre_archivo(rip_file)
            control.append(self._registro_control(institucion, fecha_remision, nombre, len(data)))
            files.append((nombre, '\r\n'.join(data)))
        
        files.append((self._nombre_archivo(self.CONTROL), '\r\n'.join(control)))
        return files

    def _facturas_periodo(self, desde, hasta, cliente, institucion):
        return (
            Factura.objects
                .cliente(cliente)
                .institucion(institucion)
                .prefetch_related('detalle')
                .fecha_expedicion_entre(desde, hasta)
                .select_related('institucion', 'cliente')
            )

class ContabilizacionRecibosForm(forms.Form):

    desde = forms.DateField()
    hasta = forms.DateField()
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all())
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def _obtener_recibos(self, desde, hasta, sucursal, institucion):
        recibos = (
            ReciboCaja.objects
                .no_anulados()
                .by_sucursal(sucursal)
                .fecha_entre(desde, hasta)
                .by_institucion(institucion)
        )
        return exportar_recibos(recibos, sucursal)

    def _nombre_archivo(self, desde, hasta):
        return 'recibos {}-{}.txt'.format(desde, hasta)

    def exportar(self):
        desde = self.cleaned_data['desde']
        hasta = self.cleaned_data['hasta']
        sucursal = self.cleaned_data['sucursal']
        institucion = self.cleaned_data['institucion']

        return (self._nombre_archivo(desde, hasta), self._obtener_recibos(desde, hasta, sucursal, institucion))

class ContabilidadForm(forms.Form):
    
    TERCEROS = 'T'
    RECIBOS_CAJA = 'RC'
    TIPOS = (
        (TERCEROS, TERCEROS),
        (RECIBOS_CAJA, RECIBOS_CAJA)
    )

    fecha = forms.DateField()
    tipo = forms.ChoiceField(choices=TIPOS)

    def _recibos_fecha(self, fecha):
        return ReciboCaja.objects.by_fecha(fecha)
    
    def _archivo_recibos(self, fecha):
        recibos = self._recibos_fecha(fecha)
        return exportar_recibos(recibos)
    
    def _archivo_terceros(self, fecha):
        return exportar_terceros([])

    def _nombre_archivo(self, tipo):
        if tipo == self.TERCEROS:
            return 'terceros.txt'
        
        return 'recibos.txt'
    
    def _obtener_registros(self, fecha, tipo):
        if tipo == self.TERCEROS:
            return self._archivo_terceros(fecha)
        return self._archivo_recibos(fecha)

    def exportar(self):
        tipo = self.cleaned_data['tipo']
        fecha = self.cleaned_data['fecha']

        return (self._nombre_archivo(tipo), self._obtener_registros(fecha, tipo))
