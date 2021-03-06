# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-13 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0007_auto_20180913_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='acompanante',
            name='parentesco',
            field=models.CharField(choices=[('P', 'Padre'), ('M', 'Madre'), ('H', 'Hermano'), ('I', 'Hijo'), ('A', 'Abuelo'), ('T', 'Tio'), ('PR', 'Primo'), ('C', 'Conyugue'), ('AM', 'Amigo'), ('O', 'Otro')], default='P', max_length=3, verbose_name='parentesco'),
            preserve_default=False,
        ),
    ]
