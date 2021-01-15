# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-25 15:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('historias', '0009_auto_20190819_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formato',
            options={'permissions': [('can_add_triage', 'Puede agregar triage'), ('can_add_goniometria', 'Puede agregar goniometria'), ('can_add_recetario_umri', 'Puede agregar recetario umri'), ('can_add_consentimiento', 'Puede agregar consentimiento'), ('can_add_terapia_fisica', 'Puede agregar terapia fisica'), ('can_add_historia_clinica', 'Puede agregar historia clinica'), ('can_add_terapia_lenguaje', 'Puede agregar terapia lenguaje'), ('can_add_nota_enfermeria', 'Puede agregar nota de enfermeria'), ('can_add_historia_escaneada', 'Puede agregar historia escaneada'), ('can_add_terapia_ocupacional', 'Puede agregar terapia ocupacional'), ('can_add_terapia_respiratoria', 'Puede agregar terapia respiratoria'), ('can_add_historia_nutricional', 'Puede agregar historia nutricional'), ('can_add_solicitud_documento', 'Puede agregar solicitud de documento'), ('can_add_formato_fonoaudiologia', 'Puede agregar formato de fonoaudiologia'), ('can_add_historia_clinica_estetica', 'Puede agregar historia clinica estetica'), ('can_add_formato_electromiografia', 'Puede agregar formato de electromiografia'), ('can_add_historia_clinica_traccion', 'Puede agregar historia clinica de traccion'), ('can_add_historia_clinica_fisiatria', 'Puede agregar historia clinica de fisiatria'), ('can_add_historia_drenaje_linfatico', 'Puede agregar historia de drenaje linfatico'), ('can_add_historia_clinica_psicologica', 'Puede agregar historia clinica psicologica'), ('can_add_formato_bloqueo_infiltracion', 'Puede agregar formato de bloqueo e infiltracion'), ('can_add_historia_clinica_estetica_corporal', 'Puede agregar historia clinica estetica corporal')], 'verbose_name': 'formato', 'verbose_name_plural': 'formatos'},
        ),
    ]