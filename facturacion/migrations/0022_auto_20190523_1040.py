# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-23 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0021_auto_20190517_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factura',
            options={'permissions': [('can_facturar', 'Puede facturar')], 'verbose_name': 'factura', 'verbose_name_plural': 'facturas'},
        ),
    ]
