# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-09 18:25
from __future__ import unicode_literals

from django.db import migrations

def add_sucursal_medico(apps, schema_editor):
    """Agrega la sucursal del medico al horario de atencion"""

    Medico = apps.get_model('organizacional', 'Empleado')
    for medico in Medico.objects.all():
        medico.horarios_atencion.all().update(sucursal=medico.sucursal)

class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0004_horarioatencion_sucursal'),
    ]

    operations = [
        migrations.RunPython(add_sucursal_medico, reverse_code=migrations.RunPython.noop)
    ]
