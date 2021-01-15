from django import forms
from agenda.models import Cita
from servicios.models import Tipo, Cliente
from organizacional.models import Institucion, Sucursal
from pacientes.models import ServicioRealizar, Paciente

class CertificadoAsistenciaForm(forms.Form):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all())
    tratamientos = forms.ModelMultipleChoiceField(queryset=ServicioRealizar.objects.all())

    def report_data(self):
        paciente = self.cleaned_data.get('paciente')
        tratamientos = self.cleaned_data.get('tratamientos')

        sucursales = Sucursal.objects.filter(citas__servicio_prestado__in=tratamientos).distinct()
        tratamientos = tratamientos.select_related('orden__institucion', 'orden__plan__cliente')
        institucion = tratamientos[0].orden.institucion
        entidad = ' - '.join(map(lambda t: str(t.entidad), tratamientos))
        citas = (
            Cita.objects
                .atendidas()
                .filter(servicio_prestado__in=tratamientos)
                .select_related('medico', 'servicio_prestado__servicio')
        )

        return (institucion, paciente, citas, sucursales, entidad)

class OportunidadCitaForm(forms.Form):
    desde = forms.DateField()
    hasta = forms.DateField()
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def _build_data(self, citas):
        result = {}
        for cita in citas:
            dias_diff = abs(cita.fecha_deseada - cita.inicio.date()).days
            key = '{}'.format(cita.empresa.cliente_id)
            if key in result:
                result[key]['cantidad'] = result[key]['cantidad'] + 1
                result[key]['dias'] = result[key]['dias'] + dias_diff
            else:
                result[key] = { 'nombre': str(cita.empresa.cliente), 'dias': dias_diff, 'cantidad': 1 }
        
        return result

    def report_data(self):
        desde = self.cleaned_data.get('desde', None)
        hasta = self.cleaned_data.get('hasta', None)
        institucion = self.cleaned_data.get('institucion', None)

        citas = (
            Cita.objects
                .fecha_entre(desde, hasta)
                .by_institucion(institucion)
                .select_related('servicio_prestado__orden__plan__cliente')
        )
        base_data = self._build_data(citas)
        total_dias = sum(d['dias'] for d in base_data.values())
        total_citas = sum(d['cantidad'] for d in base_data.values())
        indicador = total_dias / total_citas

        data = {
            'indicador': indicador,
            'total_dias': total_dias,
            'total_citas': total_citas,
            'entidades': base_data.values(),
        }
        return (desde, hasta, institucion, data)

class CitasServicioEntidadForm(forms.Form):
    desde = forms.DateField()
    hasta = forms.DateField()
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())

    def report_data(self):
        desde = self.cleaned_data.get('desde', None)
        hasta = self.cleaned_data.get('hasta', None)
        institucion = self.cleaned_data.get('institucion', None)

        entidades = Cliente.objects.all().order_by('nombre')
        servicios = Tipo.objects.in_indicadores().order_by('nombre')
        citas = (
            Cita.objects
            .atendidas()
            .fecha_entre(desde, hasta)
            .by_institucion(institucion)
            .select_related('servicio_prestado__orden__plan', 'servicio_prestado__servicio')
        )
        base_data, totales = self._build_data(citas)

        data = {
            'entidades': entidades,
            'servicios': servicios,
            'totales': self._format_totales(totales, servicios),
            'valores': self._format_cantidades(base_data, entidades, servicios),
        }
        return (desde, hasta, institucion, data)

    def _build_data(self, citas):
        result = {}
        totales = {}
        for cita in citas:
            key = '{}'.format(cita.empresa.cliente_id)
            key_servicio = '{}'.format(cita.servicio_prestado.servicio.tipo_id)
            if key in result:
                if key_servicio in result[key]:
                    result[key][key_servicio]  = result[key][key_servicio] + 1
                else:
                    result[key][key_servicio] = 1
            else:
                servicios = {}
                servicios[key_servicio] = 1
                result[key] = servicios
            
            if key_servicio in totales:
                totales[key_servicio] = totales[key_servicio] + 1
            else:
                totales[key_servicio] = 1

        return result, totales
    
    def _format_cantidades(self, data, entidades, servicios):
        _data = {}
        for entidad in entidades:
            _data[entidad.id] = {'nombre': '{}'.format(entidad), 'servicios': []}
            for servicio in servicios:
                val_entidad = data.get(str(entidad.id), {})
                _data[entidad.id]['servicios'].append(val_entidad.get(str(servicio.id), 0))
        return _data.values()
    
    def _format_totales(self, totales, servicios):
        _totales = []
        for servicio in servicios:
            _totales.append(totales.get(str(servicio.id), 0))
        return _totales

class IndMortalidadMorbilidadForm(forms.Form):
    desde = forms.DateField()
    hasta = forms.DateField()
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.all())
    
    def report_data(self):
        desde = self.cleaned_data.get('desde', None)
        hasta = self.cleaned_data.get('hasta', None)
        institucion = self.cleaned_data.get('institucion', None)

        servicios = Tipo.objects.in_indicadores().order_by('nombre')
        citas = (
            Cita.objects
                .atendidas()
                .fecha_entre(desde, hasta)
                .by_institucion(institucion)
                .select_related('servicio_prestado__orden__plan', 'servicio_prestado__servicio')
        )
        total_citas = citas.count()
        base_data = self._build_data(citas)

        data = {
            'total': total_citas,
            'valores': self._format_cantidades(base_data, servicios, total_citas),
        }
        return (desde, hasta, institucion, data)

    def _build_data(self, citas):
        result = {}
        for cita in citas:
            key = '{}'.format(cita.servicio_prestado.servicio.tipo_id)
            if key in result:
                result[key] = result[key] + 1
            else:
                result[key] = 1

        return result
    
    def _format_cantidades(self, data, servicios, total_citas):
        _data = {}
        for servicio in servicios:
            cant_citas = data.get(str(servicio.id), 0)
            porcentaje = round((cant_citas / total_citas) * 100, 1)
            _data[servicio.id] = {'nombre': '{}'.format(servicio), 'cantidad': cant_citas, 'porcentaje': porcentaje}
        return _data.values()
