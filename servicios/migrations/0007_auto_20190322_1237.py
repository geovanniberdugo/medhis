# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-22 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0006_remove_cliente_instituciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarifa',
            name='iva_coopago',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=25, verbose_name='iva coopago'),
        ),
        migrations.AlterField(
            model_name='tarifa',
            name='coopago',
            field=models.DecimalField(decimal_places=15, help_text='Valor del coopago sin IVA', max_digits=25, verbose_name='coopago'),
        ),
        migrations.AlterField(
            model_name='tarifa',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifas', to='servicios.Plan', verbose_name='convenio'),
        ),
        migrations.AlterField(
            model_name='tarifa',
            name='valor',
            field=models.DecimalField(decimal_places=15, help_text='Valor que se cobra al cliente', max_digits=25, verbose_name='valor'),
        ),
    ]
