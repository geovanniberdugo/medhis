# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-04-13 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0034_auto_20191206_1625'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caja',
            options={'ordering': ['-fecha', 'id'], 'permissions': [('can_edit_caja', 'Puede editar caja'), ('can_cerrar_caja', 'Puede cerrar caja'), ('can_see_todas_cajas', 'Puede ver todas las cajas'), ('can_recibir_caja', 'Puede recibir el dinero del cierre de caja'), ('can_see_transacciones_caja', 'Puede ver transacciones asociadas a una caja')], 'verbose_name': 'caja', 'verbose_name_plural': 'cajas'},
        ),
    ]