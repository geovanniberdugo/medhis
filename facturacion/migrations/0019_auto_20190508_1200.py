# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 17:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0018_auto_20190408_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caja',
            options={'ordering': ['-fecha'], 'permissions': [('can_edit_caja', 'Puede editar caja'), ('can_cerrar_caja', 'Puede cerrar caja'), ('can_see_todas_cajas', 'Puede ver todas las cajas'), ('can_recibir_caja', 'Puede recibir el dinero del cierre de caja'), ('can_see_transacciones_caja', 'Puede ver transacciones asociadas a una caja')], 'verbose_name': 'caja', 'verbose_name_plural': 'cajas'},
        ),
    ]