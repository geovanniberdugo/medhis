# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-06 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0033_auto_20191122_0923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factura',
            options={'permissions': [('can_facturar', 'Puede facturar'), ('can_anular_facturas', 'Puede anular facturas'), ('can_eliminar_facturas', 'Puede eliminar facturas')], 'verbose_name': 'factura', 'verbose_name_plural': 'facturas'},
        ),
    ]
