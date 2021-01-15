from enum import Enum

class FinalidadConsulta(Enum):
    ATENCION_PARTO = '01'
    ATENCION_RECIEN_NACIDO = '02'
    ATENCION_FAMILIAR = '03'
    DETECCION_CRECIMIENTO = '04'
    DETECCION_JOVEN = '05'
    DETECCION_EMBARAZO = '06'
    DETECCION_ADULTO = '07'
    DETECCION_AGUDEZA_VISUAL = '08'
    DETECCION_PROFECIONAL = '09'
    NO_APLICA = '10'

    def descripcion(self):
        descripciones = {
            self.ATENCION_PARTO: 'Atención del parto',
            self.ATENCION_RECIEN_NACIDO: 'Atención del recién nacido',
            self.ATENCION_FAMILIAR: 'Atención en planificación familiar',
            self.DETECCION_CRECIMIENTO: 'Detección de alteraciones de crecimiento y desarrollo del menor de diez años',
            self.DETECCION_JOVEN: 'Detección de alteración del desarrollo joven',
            self.DETECCION_EMBARAZO: 'Detección de alteraciones del embarazo',
            self.DETECCION_ADULTO: 'Detección de alteraciones del adulto',
            self.DETECCION_AGUDEZA_VISUAL: 'Detección de alteraciones de agudeza visual',
            self.DETECCION_PROFECIONAL: 'Detección de enfermedad profesional',
            self.NO_APLICA: 'No aplica'
        }

        return descripciones[self.value]

class CausaExterna(Enum):
    ACCIDENTE_TRABAJO = '01'
    ACCIDENTE_TRANSITO = '02'
    ACCIDENTE_RABICO = '03'
    ACCIDENTE_OFIDICO = '04'
    OTRO_ACCIDENTE = '05'
    EVENTO_CATASTROFICO = '06'
    LESION_AGRESION = '07'
    LESION_AUTO_INFLIGIDA = '08'
    SOSPECHA_MALTRATO_FISICO = '09'
    SOSPECHA_ABUSO_SEXUAL = '10'
    SOSPECHA_VIOLENCIA_SEXUAL = '11'
    SOSPECHA_MALTRATO_EMOCIONAL = '12'
    ENFERMEDAD_GENERAL = '13'
    ENFERMEDAD_PROFESIONAL = '14'
    OTRA = '15'

    def descripcion(self):
        descripciones = {
            self.ACCIDENTE_TRABAJO: 'Accidente de trabajo',
            self.ACCIDENTE_TRANSITO: 'Accidente de tránsito',
            self.ACCIDENTE_RABICO: 'Accidente rábico',
            self.ACCIDENTE_OFIDICO: 'Accidente ofídico',
            self.OTRO_ACCIDENTE: 'Otro tipo de accidente',
            self.EVENTO_CATASTROFICO: 'Evento catastrófico',
            self.LESION_AGRESION: 'Lesión por agresión',
            self.LESION_AUTO_INFLIGIDA: 'Lesión auto infligida',
            self.SOSPECHA_MALTRATO_FISICO: 'Sospecha de maltrato físico',
            self.SOSPECHA_ABUSO_SEXUAL: 'Sospecha de abuso sexual',
            self.SOSPECHA_VIOLENCIA_SEXUAL: 'Sospecha de violencia sexual',
            self.SOSPECHA_MALTRATO_EMOCIONAL: 'Sospecha de maltrato emocional',
            self.ENFERMEDAD_GENERAL: 'Enfermedad general',
            self.ENFERMEDAD_PROFESIONAL: 'Enfermedad profesional',
            self.OTRA: 'Otra'
        }

        return descripciones[self.value]

class TipoDiagnostico(Enum):
    IMPRESION_DIAGNOSTICA = '1'
    CONFIRMADO_NUEVO = '2'
    CONFIRMADO_REPETIDO = '3'

    def descripcion(self):
        descripciones = {
            self.IMPRESION_DIAGNOSTICA: 'Impresión diagnostica',
            self.CONFIRMADO_NUEVO: 'Confirmado nuevo',
            self.CONFIRMADO_REPETIDO: 'Confirmado repetido',
        }

        return descripciones[self.value]

class AmbitoProcedimiento(Enum):
    AMBULATORIO = '1'
    HOSPITALARIO = '2'
    URGENCIAS = '3'

    def descripcion(self):
        descripciones = {
            self.AMBULATORIO: 'Ambulatorio',
            self.HOSPITALARIO: 'Hospitalario',
            self.URGENCIAS: 'En urgencias',
        }

        return descripciones[self.value]

class FinalidadProcedimiento(Enum):
    DIAGNOSTICO = '1'
    TERAPEUTICO = '2'
    PROTECCION_ESPECIFICA = '3'
    DETECCION_ENFERMEDAD_GENERAL = '4'
    DETECCION_ENFERMEDAD_PROFESIONAL = '5'

    def descripcion(self):
        descripciones = {
            self.DIAGNOSTICO: 'Diagnóstico',
            self.TERAPEUTICO: 'Terapéutico',
            self.PROTECCION_ESPECIFICA: 'Protección específica',
            self.DETECCION_ENFERMEDAD_GENERAL: 'Detección temprana de enfermedad general',
            self.DETECCION_ENFERMEDAD_PROFESIONAL: 'Detección temprana de enfermedad profesional',
        }

        return descripciones[self.value]

class PersonalAtiende(Enum):
    ESPECIALISTA = '1'
    GENERAL = '2'
    ENFERMERO = '3'
    AUXILIAR_ENFERMERIA = '4'
    OTRO = '5'

    def descripcion(self):
        descripciones = {
            self.ESPECIALISTA: 'Médico (a) especialista',
            self.GENERAL: 'Médico (a) general',
            self.ENFERMERO: 'Enfermera (o)',
            self.AUXILIAR_ENFERMERIA: 'Auxiliar de enfermería',
            self.OTRO: 'Otro',
        }

        return descripciones[self.value]

class FormaActoQuirurgico(Enum):
    UNICO = '1'
    MULTIPLE_MISMA_DIF_ESPECIALIDAD = '2'
    MULTIPLE_MISMA_IGUAL_ESPECIALIDAD = '3'
    MULTIPLE_DIF_DIF_ESPECIALIDAD = '4'
    MULTIPLE_DIF_IGUAL_ESPECIALIDAD = '5'

    def descripcion(self):
        descripciones = {
            self.UNICO: 'Unico o unilateral',
            self.MULTIPLE_MISMA_DIF_ESPECIALIDAD: 'Múltiple o bilateral, misma vía, diferente especialidad',
            self.MULTIPLE_MISMA_IGUAL_ESPECIALIDAD: 'Múltiple o bilateral, misma vía, igual especialidad',
            self.MULTIPLE_DIF_DIF_ESPECIALIDAD: 'Múltiple o bilateral, diferente vía, diferente especialidad',
            self.MULTIPLE_DIF_IGUAL_ESPECIALIDAD: 'Múltiple o bilateral, diferente vía, igual especialidad',
        }

        return descripciones[self.value]
