# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-19 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0016_auto_20191108_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='atenciones_simultaneas',
            field=models.PositiveIntegerField(blank=True, help_text='Pacientes que puede atender al mismo tiempo', null=True, verbose_name='atenciones simulataneas'),
        ),
    ]