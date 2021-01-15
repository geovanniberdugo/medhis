from django.contrib.postgres import fields
from django.db import models

class Rips(models.Model):
    
    CONSULTA = 'CO'
    PROCEDIMIENTO = 'PR'
    TIPOS = (
        (CONSULTA, 'Consulta'),
        (PROCEDIMIENTO, 'Procedimiento'),
    )

    tipo = models.CharField(max_length=2, choices=TIPOS, unique=True)
    data = fields.JSONField()

    class Meta:
        verbose_name = 'rips'
        verbose_name_plural = 'rips'

    def __str__(self):
        return '{}'.format(self.get_tipo_display())

class Configuracion(models.Model):

    R256_TIPO_1 = 1
    R256_TIPO_2 = 2
    R256_TIPO_3 = 3
    R256_TIPO_4 = 4
    R256_TIPO_5 = 5
    R256_TIPO_6 = 6

    resolucion_256 = fields.ArrayField(
        null=True,
        blank=True,
        base_field=models.IntegerField(),
        help_text='tipos de registro que no aplican para el tenant'
    )

    class Meta:
        verbose_name = 'configuración'
        verbose_name_plural = 'configuraciones'
