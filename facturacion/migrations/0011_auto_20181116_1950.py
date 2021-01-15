# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 00:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0010_auto_20181115_1237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caja',
            options={'ordering': ['-fecha'], 'permissions': [('puede_cerrar_caja', 'Puede cerrar caja'), ('puede_ver_caja', 'Puede ver detalle de una caja'), ('puede_ver_todas_cajas', 'Puede ver todas las cajas'), ('puede_recibir_caja', 'Puede recibir el cierre de caja'), ('puede_ver_transacciones', 'Puede ver transacciones asociadas a una caja')], 'verbose_name': 'caja', 'verbose_name_plural': 'cajas'},
        ),
    ]
