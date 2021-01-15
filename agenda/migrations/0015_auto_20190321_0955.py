# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-21 14:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0014_auto_20190314_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cita',
            options={'ordering': ['inicio'], 'permissions': [('puede_ver_agenda', 'Puede ver la agenda'), ('puede_agendar_cita', 'Puede agendar citas'), ('can_see_todas_citas', 'Puede ver todas las citas'), ('puede_ver_todas_citas', 'Puede ver todas las citas'), ('can_see_agenda_diaria', 'Puede ver la agenda diaria'), ('puede_cambiar_estado', 'Puede cambiar el estado de una cita'), ('puede_generar_indicadores_resolucion_256', 'Puede generar los indicadores para la resolucion 256'), ('can_set_cumplida_dia_diferente', 'Puede cambiar el estado a cumplida sin que la fecha de la cita sea el dia actual')], 'verbose_name': 'cita', 'verbose_name_plural': 'citas'},
        ),
    ]
