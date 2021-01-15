# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-10 21:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_auto_20180907_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='anulada',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='razon_anulacion',
        ),
        migrations.RemoveField(
            model_name='serviciorealizar',
            name='numero_sesiones',
        ),
        migrations.AddField(
            model_name='serviciorealizar',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, verbose_name='cantidad'),
        ),
        migrations.AlterField(
            model_name='orden',
            name='afiliacion',
            field=models.CharField(blank=True, choices=[('C', 'Cotizante'), ('B', 'Beneficiario'), ('A', 'Subsidiado'), ('P', 'Particular'), ('V', 'Vinculado'), ('O', 'Otro')], max_length=1, verbose_name='afiliación'),
        ),
        migrations.AlterField(
            model_name='orden',
            name='institucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordenes', to='organizacional.Institucion', verbose_name='entidad que prestará el servicio'),
        ),
        migrations.AlterField(
            model_name='orden',
            name='tipo_usuario',
            field=models.CharField(blank=True, choices=[('C', 'Contributivo'), ('A', 'Subsidiado'), ('V', 'Vinculado'), ('P', 'Particular'), ('O', 'Otro')], max_length=1, verbose_name='tipo de usuario'),
        ),
        migrations.AlterField(
            model_name='serviciorealizar',
            name='coopago',
            field=models.DecimalField(decimal_places=15, default=0, help_text='Coopago por sesión', max_digits=25, verbose_name='coopago/moderadora'),
        ),
        migrations.AlterField(
            model_name='serviciorealizar',
            name='valor',
            field=models.DecimalField(decimal_places=15, default=0, help_text='Valor por sesión', max_digits=25, verbose_name='valor'),
        ),
    ]