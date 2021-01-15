import factory
from .. import models


class FormatoFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Formato
        django_get_or_create = ('nombre',)

    nombre = 'HISTORIA CLINICA'
    contenido = {
        "order": ["consulta"],
        "consulta": {
            "fields": {
                "order": ["motivoConsulta", "enfermedadActual"],
                "motivoConsulta": {"tipo": "text", "nombre": "Motivo de consulta", "required": True},
                "enfermedadActual": {"tipo": "textarea", "nombre": "Enfermedad actual"}
            },
            "nombre": "Consulta"
        }
    }


class HistoriaFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Historia

    proveedor = factory.SubFactory('organizacional.tests.factories.MedicoFactory')
    formato = factory.SubFactory(FormatoFactory)
    contenido = {
        "order": ["consulta"],
        "consulta": {
            "fields": {
                "order": ["motivoConsulta", "enfermedadActual"],
                "motivoConsulta": {"tipo": "text", "nombre": "Motivo de consulta", "required": True},
                "enfermedadActual": {"tipo": "textarea", "nombre": "Enfermedad actual"}
            },
            "nombre": "Consulta"
        }
    }
    data = {
        "consulta": {
            "motivoConsulta": "Dolor de cabeza",
            "enfermedadActual": "Dolor de cabeza frecuente"
        }
    }


class AdjuntoFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Adjunto

    historia = factory.SubFactory(HistoriaFactory)
    archivo = factory.django.FileField()
