# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-22 20:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0002_auto_20190813_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reporte',
            options={'managed': False, 'permissions': [('can_see_citas_paciente', 'Puede ver reporte citas por paciente'), ('can_see_relacion_recibos_caja', 'Puede ver relacion recibos de caja'), ('can_see_certificado_asistencia', 'Puede ver certificado de asistencia'), ('can_see_tratamientos_facturado_entidad', 'Puede ver reporte tratamientos facturados por entidad'), ('can_see_tratamientos_pago_profesional', 'Puede ver relacion de tratamientos para pago de profesional'), ('can_see_tratamientos_iniciados_profesional', 'Puede ver reporte tratamientos iniciados por profesional'), ('can_see_tratamientos_terminado_profesional', 'Puede ver reporte tratamientos terminados por profesional'), ('can_see_tratamientos_no_terminado_profesional', 'Puede ver reporte tratamientos no terminados por profesional')]},
        ),
    ]
