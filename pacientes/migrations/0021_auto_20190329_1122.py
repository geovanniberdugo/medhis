# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0020_auto_20190321_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviciorealizar',
            name='is_coopago_total',
            field=models.BooleanField(default=False, help_text='Indica si el valor del coopago es por todas las sesiones'),
        ),
        migrations.AlterField(
            model_name='serviciorealizar',
            name='coopago',
            field=models.DecimalField(decimal_places=15, default=0, help_text='Coopago por sesión o total según is_coopago_total', max_digits=25, verbose_name='coopago/moderadora'),
        ),
    ]