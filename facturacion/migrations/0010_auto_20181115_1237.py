# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-15 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
        ('facturacion', '0009_auto_20181115_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caja',
            options={'ordering': ['-fecha'], 'permissions': [('puede_cerrar_caja', 'Puede cerrar caja'), ('puede_ver_caja', 'Puede ver detalle de una caja'), ('puede_ver_todas_cajas', 'Puede ver todas las cajas')], 'verbose_name': 'caja', 'verbose_name_plural': 'cajas'},
        ),
        migrations.AddField(
            model_name='caja',
            name='recibido_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caja',
            name='recibido_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cajas_recibidas', to='organizacional.Empleado'),
        ),
    ]
