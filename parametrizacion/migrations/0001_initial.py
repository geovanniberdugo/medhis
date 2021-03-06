# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-11 21:10
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('CO', 'Consulta'), ('PR', 'Procedimiento')], max_length=2)),
                ('contenido', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'verbose_name': 'rips',
                'verbose_name_plural': 'rips',
            },
        ),
    ]
