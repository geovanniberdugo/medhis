# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-15 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0008_auto_20181109_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecaja',
            name='forma_pago',
            field=models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta'), ('O', 'Otros')], max_length=2, verbose_name='forma de pago'),
        ),
        migrations.AlterField(
            model_name='recibocaja',
            name='forma_pago',
            field=models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta')], max_length=2, verbose_name='forma de pago'),
        ),
    ]
