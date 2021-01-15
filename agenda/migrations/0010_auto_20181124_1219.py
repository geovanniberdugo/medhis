# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-24 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0009_auto_20181124_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='horario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='agenda.HorarioAtencion', verbose_name='horario'),
        ),
    ]
