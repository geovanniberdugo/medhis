# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-05 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0029_auto_20191028_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrofacturasiigo',
            name='codigo_linea',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='parametrofacturasiigo',
            name='codigo_producto',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
