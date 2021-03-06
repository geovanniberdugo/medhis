# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-28 22:29
from __future__ import unicode_literals

import common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('duracion', models.DurationField(help_text='Duración de la atención para cada cita. Ingresar duración de la forma HH:MM:SS', verbose_name='duración')),
            ],
            options={
                'verbose_name': 'agenda',
                'verbose_name_plural': 'agendas',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creada_el', models.DateTimeField(auto_now_add=True, verbose_name='fecha llamada')),
                ('fecha_deseada', models.DateField(blank=True, null=True, verbose_name='fecha deseada')),
                ('autorizacion', models.CharField(blank=True, max_length=100, verbose_name='autorización')),
                ('fecha_autorizacion', models.DateField(blank=True, null=True, verbose_name='Fecha de autorización')),
            ],
            options={
                'verbose_name': 'cita',
                'verbose_name_plural': 'citas',
                'ordering': ['horario__start'],
                'permissions': [('puede_ver_agenda', 'Puede ver la agenda'), ('puede_agendar_cita', 'Puede agendar citas'), ('puede_ver_todas_citas', 'Puede ver todas las citas'), ('puede_cambiar_estado', 'Puede cambiar el estado de una cita'), ('puede_generar_indicadores_resolucion_256', 'Puede generar los indicadores para la resolucion 256')],
            },
            bases=(common.models.UpdateModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistorialEstado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('NC', 'No confirmada'), ('CO', 'Confirmada'), ('CU', 'Cumplida'), ('TE', 'Atendida'), ('CA', 'Cancelada'), ('EX', 'Excusada'), ('NA', 'No asistio')], max_length=2, verbose_name='estado')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
            ],
            options={
                'verbose_name': 'historial estado',
                'verbose_name_plural': 'historial estados',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='HorarioAtencion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, verbose_name='titulo')),
                ('start', models.DateTimeField(verbose_name='inicio')),
                ('end', models.DateTimeField(verbose_name='final')),
            ],
            options={
                'verbose_name': 'horario de atención',
                'verbose_name_plural': 'horarios de atención',
            },
        ),
    ]
