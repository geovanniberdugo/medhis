# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-28 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0024_auto_20190802_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha_expedicion',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de expedicion'),
        ),
    ]