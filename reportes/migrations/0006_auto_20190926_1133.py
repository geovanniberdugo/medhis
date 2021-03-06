# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-26 16:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0005_auto_20190920_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reporte',
            options={'managed': False, 'permissions': [('can_see_citas_paciente', 'Puede ver reporte citas por paciente'), ('can_see_relacion_recibos_caja', 'Puede ver relacion recibos de caja'), ('can_see_asignacion_citas', 'Puede ver reporte de asignacion de citas'), ('can_see_citas_no_cumplidas', 'Puede ver reporte de citas no cumplidas'), ('can_see_certificado_asistencia', 'Puede ver certificado de asistencia'), ('can_see_facturas_entidad', 'Puede ver reporte de facturas por entidad'), ('can_see_medicos_ordenan_tratamiento', 'Puede ver reporte de medicos que ordenan tratamiento'), ('can_see_tratamientos_facturado_entidad', 'Puede ver reporte tratamientos facturados por entidad'), ('can_see_tratamientos_pago_profesional', 'Puede ver relacion de tratamientos para pago de profesional'), ('can_see_tratamientos_iniciados_profesional', 'Puede ver reporte tratamientos iniciados por profesional'), ('can_see_tratamientos_terminado_profesional', 'Puede ver reporte tratamientos terminados por profesional'), ('can_see_tratamientos_no_terminado_profesional', 'Puede ver reporte tratamientos no terminados por profesional')]},
        ),
    ]
