# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-20 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0012_auto_20181116_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecaja',
            name='forma_pago',
            field=models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta')], max_length=2, verbose_name='forma de pago'),
        ),
    ]
