# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-11 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0010_tipo_in_indicadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='puc_facturacion',
            field=models.CharField(blank=True, max_length=100, verbose_name='cuenta puc facturacion'),
        ),
    ]