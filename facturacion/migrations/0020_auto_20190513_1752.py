# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-13 22:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0019_auto_20190508_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
