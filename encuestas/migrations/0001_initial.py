# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-28 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventoAdverso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='fecha del evento')),
                ('caida', models.CharField(choices=[('1', 'ninguno'), ('2', 'hospitalizacion'), ('3', 'urgencias'), ('4', 'consulta externa'), ('5', 'apoyo diagnostico')], default='1', max_length=1)),
                ('tipo_caida', models.CharField(choices=[('1', 'ninguno'), ('2', 'evento adverso'), ('3', 'incidente')], default='1', max_length=1)),
                ('medicamentos', models.CharField(choices=[('1', 'ninguno'), ('2', 'hospitalizacion'), ('3', 'urgencias'), ('4', 'ulcera')], default='1', max_length=1)),
                ('paciente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventos_adversos', to='pacientes.Paciente', verbose_name='paciente')),
            ],
        ),
        migrations.CreateModel(
            name='SatisfaccionGlobal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='fecha de la encuesta')),
                ('pregunta1', models.CharField(choices=[('2', 'Muy Buena'), ('3', 'Buena'), ('4', 'Regular'), ('5', 'Mala'), ('6', 'Muy Mala'), ('1', 'No Responde')], default='1', max_length=1)),
                ('pregunta2', models.CharField(choices=[('2', 'Definitivamente Si'), ('3', 'Probablemente Si'), ('4', 'Definitivamente No'), ('5', 'Probablemente No'), ('1', 'No Responde')], default='1', max_length=1)),
                ('paciente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='satisfaccion_global', to='pacientes.Paciente', verbose_name='paciente')),
            ],
            options={
                'verbose_name': 'Encuesta de Satisfaccion Global',
                'verbose_name_plural': 'Encuestas de Satisfaccion Global',
                'permissions': [('puede_ver_encuesta', 'Puede ver la encuesta'), ('puede_crear_encuesta', 'Puede crear una encuesta')],
            },
        ),
    ]
