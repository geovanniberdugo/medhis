from django.utils.translation import ugettext_lazy as _lazy
from django.db import models
from .managers import SatisfaccionGlobalManager, EventoAdversoManager

class SatisfaccionGlobal(models.Model):
    """Modelo para guardar la información de encuesta Resolucion 256 de 2016."""

    NO_RESPONDE = '1'
    MUY_BUENA = '2'
    BUENA = '3'
    REGULAR = '4'
    MALA = '5'
    MUY_MALA = '6'

    OPCIONES1 = (
        (MUY_BUENA, _lazy('Muy Buena')),
        (BUENA, _lazy('Buena')),
        (REGULAR, _lazy('Regular')),
        (MALA, _lazy('Mala')),
        (MUY_MALA, _lazy('Muy Mala')),
        (NO_RESPONDE, _lazy('No Responde')),
    )

    DEFINITIVAMENTE_SI = '2'
    PROBABLEMENTE_SI = '3'
    DEFINITIVAMENTE_NO = '4'
    PROBABLEMENTE_NO = '5'

    OPCIONES2 = (
        (DEFINITIVAMENTE_SI, _lazy('Definitivamente Si')),
        (PROBABLEMENTE_SI, _lazy('Probablemente Si')),
        (DEFINITIVAMENTE_NO, _lazy('Definitivamente No')),
        (PROBABLEMENTE_NO, _lazy('Probablemente No')),
        (NO_RESPONDE, _lazy('No Responde')),
    )

    paciente = models.ForeignKey('pacientes.Paciente', related_name='satisfaccion_global', verbose_name=_lazy('paciente'), null=True, blank=True)
    fecha = models.DateField(_lazy('fecha de la encuesta'), auto_now_add=True)
    pregunta1 = models.CharField(max_length=1, default=NO_RESPONDE, choices=OPCIONES1)
    pregunta2 = models.CharField(max_length=1, default=NO_RESPONDE, choices=OPCIONES2)

    objects = SatisfaccionGlobalManager()

    class Meta:
        verbose_name = 'Encuesta de Satisfaccion Global'
        verbose_name_plural = 'Encuestas de Satisfaccion Global'
        permissions = [
            ('puede_ver_encuesta', 'Puede ver la encuesta'),
            ('puede_crear_encuesta', 'Puede crear una encuesta')
        ]

class EventoAdverso(models.Model):
    """Modelo para registrar eventos adversos de acuerdo a la Resolucion 256 de 2016."""

    NINGUNO = '1'
    HOSPITALIZACION = '2'
    URGENCIAS = '3'
    CONSULTA_EXTERNA = '4'
    APOYO_DIAGNOSTICO = '5'
    CAIDAS = (
        (NINGUNO, _lazy('ninguno')),
        (HOSPITALIZACION, _lazy('hospitalizacion')),
        (URGENCIAS, _lazy('urgencias')),
        (CONSULTA_EXTERNA, _lazy('consulta externa')),
        (APOYO_DIAGNOSTICO, _lazy('apoyo diagnostico')),
    )

    EVENTO_ADVERSO = '2'
    INCIDENTE = '3'
    CALIFICACION_CAIDA = (
        (NINGUNO, _lazy('ninguno')),
        (EVENTO_ADVERSO, _lazy('evento adverso')),
        (INCIDENTE, _lazy('incidente')),
    )

    ULCERA = '4'
    MEDICAMENTOS = (
        (NINGUNO, _lazy('ninguno')),
        (HOSPITALIZACION, _lazy('hospitalizacion')),
        (URGENCIAS, _lazy('urgencias')),
        (ULCERA, _lazy('ulcera')),
    )

    paciente = models.ForeignKey('pacientes.Paciente', related_name='eventos_adversos', verbose_name=_lazy('paciente'), null=True, blank=True)
    fecha = models.DateField(_lazy('fecha del evento'), auto_now_add=True)
    caida = models.CharField(max_length=1, default=NINGUNO, choices=CAIDAS)
    tipo_caida = models.CharField(max_length=1, default=NINGUNO, choices=CALIFICACION_CAIDA)
    medicamentos = models.CharField(max_length=1, default=NINGUNO, choices=MEDICAMENTOS)
    
    objects = EventoAdversoManager()
    
    def __str__(self):
        return self.caida
    
