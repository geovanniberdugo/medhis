# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-20 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0012_institucion_footer_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='universidad',
            field=models.CharField(blank=True, max_length=100, verbose_name='universidad historia'),
        ),
    ]
