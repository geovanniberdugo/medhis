# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-05 16:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0010_auto_20181004_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serviciorealizar',
            options={'permissions': [('puede_recibir_asistencia', 'Puede recibir la asistencia entregada por los medicos'), ('puede_verificar_asistencia', 'Puede verificar la asistencia entregada por los medicos')], 'verbose_name': 'servicio a realizar', 'verbose_name_plural': 'servicios a realizar'},
        ),
    ]
