# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-26 22:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0027_sucusales_recibo_20190926_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibocaja',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibos_caja', to='organizacional.Sucursal'),
        ),
    ]