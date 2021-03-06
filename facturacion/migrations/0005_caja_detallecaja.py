# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-07 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
        ('facturacion', '0004_factura_paciente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cajas', to='organizacional.Empleado')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cajas', to='organizacional.Sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_pago', models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta'), ('C', 'Consignación')], max_length=2, verbose_name='forma de pago')),
                ('valor', models.DecimalField(decimal_places=15, max_digits=25, verbose_name='valor')),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='facturacion.Caja')),
            ],
        ),
    ]
