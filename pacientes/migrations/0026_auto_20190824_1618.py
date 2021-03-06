# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-24 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0025_auto_20190713_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='direccion_empresa',
            field=models.CharField(blank=True, max_length=100, verbose_name='direccion empresa'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='empresa',
            field=models.CharField(blank=True, max_length=100, verbose_name='empresa donde labora'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='telefono2',
            field=models.CharField(blank=True, max_length=100, verbose_name='telefono2'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='telefono_empresa',
            field=models.CharField(blank=True, max_length=100, verbose_name='telefono empresa'),
        ),
    ]
