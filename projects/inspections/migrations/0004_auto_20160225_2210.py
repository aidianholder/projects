# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0003_auto_20160225_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
