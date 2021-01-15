from django import forms
from django.db.models import Q, Count
from organizacional.models import Institucion, Empleado, Sucursal
from encuestas.models import SatisfaccionGlobal, EventoAdverso
from parametrizacion.models import Configuracion
from pacientes.models import Paciente
from .models import Cita


class IndicadoresResolucion256Form(forms.Form):
    """"""

    TIPO2 = ['890201', '890203', '890202', ('881112', '882841'), ('883101', '883910')]
    TIPO4 = [('010101', '869700')]

    desde = forms.DateField()
    hasta = forms.DateField()
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def _filtros_cups(self, cups):
        query = Q()
        for cup in cups:
            if isinstance(cup, tuple):
                q = Q(servicio_prestado__servicio__cups__range=cup)
            else:
                q = Q(servicio_prestado__servicio__cups=cup)
            
            query = query | q
        return query

    def _fecha_inicial(self):
        return self.cleaned_data['desde'].strftime('%Y%m%d')
    
    def _fecha_final(self):
        return self.cleaned_data['hasta'].strftime('%Y%m%d')

    def _format_text(self, value):
        return value.upper().replace('Ñ', 'N')

    def _formato_nit_institucion(self, nit):
        return '{:0>12}'.format(nit)
    
    def _formato_fecha(self, fecha):
        if fecha:
            return fecha.strftime('%Y-%m-%d')
        
        return ''
    
    def _formato_genero(self, genero):
        if genero == Paciente.MASCULINO:
            return 'H'
        elif genero == Paciente.FEMENINO:
            return 'M'
        else:
            return 'I'
    
    def _total_encuesta(self, pregunta, respuestas, valor):
        return next((p['total'] for p in respuestas if p[pregunta] == valor), 0)

    def _registro_tipo1(self, institucion, total_registros):
        return [
            1,
            institucion.codigo,
            'NI',
            institucion.nit_sin_digito_verificacion(),
            self._fecha_inicial(),
            self._fecha_final(),
            total_registros
        ]
    
    def _filtrar_tipo2(self, citas):
        primeras_citas = {}
        for cita in citas:
            key = '{}-{}'.format(cita.paciente.id, cita.servicio_prestado.servicio.id)
            if key in primeras_citas:
                if cita.inicio < primeras_citas[key].inicio:
                    primeras_citas[key] = cita
            else:
                primeras_citas[key] = cita
        
        return map(lambda key: primeras_citas[key], primeras_citas.keys())

    def _registro_tipo2(self, consecutivo, cita):
        paciente = cita.paciente
        cliente = cita.empresa.cliente

        return [
            2,
            consecutivo,
            paciente.tipo_documento,
            paciente.numero_documento.upper(),
            self._formato_fecha(paciente.fecha_nacimiento),
            self._formato_genero(paciente.genero),
            self._format_text(paciente.primer_apellido),
            self._format_text(paciente.segundo_apellido),
            self._format_text(paciente.primer_nombre),
            self._format_text(paciente.segundo_nombre),
            cliente.codigo,
            1, # TODO cups se coloca 1 momentaneamente revisar norma
            self._formato_fecha(cita.creada_el),
            1,  # TODO cita asignada 1: si o 2: no
            self._formato_fecha(cita.inicio),
            '' # self._formato_fecha(cita.fecha_deseada) se quita por peticion de la doctora
        ]

    def _registro_tipo3(self, consecutivo, institucion, pregunta1, pregunta2):
        return [
            3,
            consecutivo,
            'NI',
            institucion.nit_sin_digito_verificacion(),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.MUY_BUENA),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.BUENA),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.REGULAR),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.MALA),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.MUY_MALA),
            self._total_encuesta('pregunta1', pregunta1, SatisfaccionGlobal.NO_RESPONDE),
            self._total_encuesta('pregunta2', pregunta2, SatisfaccionGlobal.DEFINITIVAMENTE_SI),
            self._total_encuesta('pregunta2', pregunta2, SatisfaccionGlobal.PROBABLEMENTE_SI),
            self._total_encuesta('pregunta2', pregunta2, SatisfaccionGlobal.DEFINITIVAMENTE_NO),
            self._total_encuesta('pregunta2', pregunta2, SatisfaccionGlobal.PROBABLEMENTE_NO),
            self._total_encuesta('pregunta2', pregunta2, SatisfaccionGlobal.NO_RESPONDE)
        ]
    
    def _registro_tipo4(self, consecutivo, cita):
        paciente = cita.paciente
        cliente = cita.empresa.cliente

        return [
            4,
            consecutivo,
            paciente.tipo_documento,
            paciente.numero_documento.upper(),
            self._formato_fecha(paciente.fecha_nacimiento),
            self._formato_genero(paciente.genero),
            self._format_text(paciente.primer_apellido),
            self._format_text(paciente.segundo_apellido),
            self._format_text(paciente.primer_nombre),
            self._format_text(paciente.segundo_nombre),
            cliente.codigo,
            'CODIGO MUNICIPIO RESIDENCIA PACIENTE',  # TODO preguntar por esto al ingresar la cita
            cita.servicio.cups,
            self._formato_fecha(cita.creada_el),
            self._formato_fecha(cita.inicio),
            'SI O NO SE REALIZO PROCEDIMIENTO'  # TODO sacar esto de la cita si fue atendida o no
            ''  # TODO preguntar por esto CAUSA DE NO REALIZACION
            'SI O NO SE REPROGRAMO PROCEDIMIENTO'  # TODO preguntar en algun lado
        ]

    def _registro_tipo5(self, consecutivo, institucion, caidas_lugar, caidas_tipo, medicamentos):
        return [
            5,
            consecutivo,
            'NI',
            institucion.nit_sin_digito_verificacion(),
            self._total_encuesta('caida', caidas_lugar, EventoAdverso.HOSPITALIZACION),
            self._total_encuesta('caida', caidas_lugar, EventoAdverso.URGENCIAS),
            self._total_encuesta('caida', caidas_lugar, EventoAdverso.CONSULTA_EXTERNA),
            self._total_encuesta('caida', caidas_lugar, EventoAdverso.APOYO_DIAGNOSTICO),
            self._total_encuesta('tipo_caida', caidas_tipo, EventoAdverso.EVENTO_ADVERSO),
            self._total_encuesta('tipo_caida', caidas_tipo, EventoAdverso.INCIDENTE),
            self._total_encuesta('medicamentos', medicamentos, EventoAdverso.HOSPITALIZACION),
            self._total_encuesta('medicamentos', medicamentos, EventoAdverso.URGENCIAS),
            self._total_encuesta('medicamentos', medicamentos, EventoAdverso.ULCERA)
        ]

    def nombre_archivo(self):
        institucion = self.cleaned_data['institucion']
        return 'MCA195MOCA{}NI{}C{:0>2}.txt'.format(
            self._fecha_final(),
            self._formato_nit_institucion(institucion.nit_sin_digito_verificacion()),
            1  # TODO Consecutivo debe variar si el tenant tiene sucursales principales en distintos municipios
        )
    
    def generar_datos(self):
        desde = self.cleaned_data['desde']
        hasta = self.cleaned_data['hasta']
        institucion = self.cleaned_data['institucion']

        consecutivo = 1
        config = getattr(Configuracion.objects.first(), 'resolucion_256', None)

        registros2 = []
        if not config or Configuracion.R256_TIPO_2 not in config:
            citas = (
                Cita.objects
                    .paciente_creado(desde, hasta)
                    .filter(self._filtros_cups(self.TIPO2))
                    .select_related('servicio_prestado__orden__plan__cliente', 'servicio_prestado__orden__paciente', 'servicio_prestado__servicio')
                )
            registros2 = list(map(
                lambda o: self._registro_tipo2(o[0], o[1]),
                enumerate(self._filtrar_tipo2(citas), start=consecutivo)
            ))        
            consecutivo = len(registros2) + 1
        
        registros3 = []
        if not config or Configuracion.R256_TIPO_3 not in config:
            registros_satisfaction_global = SatisfaccionGlobal.objects.rango_fechas(desde, hasta)
            pregunta1 = registros_satisfaction_global.values('pregunta1').annotate(total=Count('id'))
            pregunta2 = registros_satisfaction_global.values('pregunta2').annotate(total=Count('id'))
            registros3 = [self._registro_tipo3(consecutivo, institucion, pregunta1, pregunta2)]
            consecutivo = consecutivo + 1
        
        registros4 = []
        if not config or Configuracion.R256_TIPO_4 not in config:
            citas = Cita.objects.fecha_entre(desde, hasta).filter(self._filtros_cups(self.TIPO4))
            registros4 = list(map(
                lambda o: self._registro_tipo4(o[0], o[1]),
                enumerate(citas, start=consecutivo)
            ))
            consecutivo = consecutivo + len(registros4)

        registros5 = []
        if not config or Configuracion.R256_TIPO_5 not in config:
            eventos = EventoAdverso.objects.rango_fechas(desde, hasta)
            caidas_lugar = eventos.values('caida').annotate(total=Count('id'))
            caidas_tipo = eventos.values('tipo_caida').annotate(total=Count('id'))
            medicamentos = eventos.values('medicamentos').annotate(total=Count('id'))
            registros5 = [self._registro_tipo5(consecutivo, institucion, caidas_lugar, caidas_tipo, medicamentos)]

        data = registros2 + registros3 + registros4 + registros5
        registros1 = [self._registro_tipo1(institucion, len(data) + 1)]
        return registros1 + data
    
class AgendaDiariaForm(forms.Form):

    fecha = forms.DateField()
    medico = forms.ModelChoiceField(
        required=False,
        queryset=Empleado.objects.medicos()
    )
    sucursal = forms.ModelChoiceField(
        required=False,
        queryset=Sucursal.objects.all()
    )

    def get_data(self):
        fecha = self.cleaned_data.get('fecha', None)
        medico = self.cleaned_data.get('medico', None)
        sucursal = self.cleaned_data.get('sucursal', None)
        
        return (fecha, medico, sucursal)

    def citas_dia(self):
        fecha, medico, sucursal = self.get_data()
        citas = Cita.objects.by_fecha(fecha)

        if medico:
            with_medico = []
            citas = citas.by_medico(medico)
        else:
            with_medico = ['medico']
        
        if sucursal:
            citas = citas.by_sucursal(sucursal)
        
        citas = citas.select_related(
            'servicio_prestado__servicio',
            'servicio_prestado__orden__plan',
            'servicio_prestado__orden__paciente',
            'servicio_prestado__orden__institucion',
            'servicio_prestado__orden__plan__cliente',
            *with_medico
        ).annotate_estado()
        return citas
