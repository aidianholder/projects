# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 00:09
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0009_auto_20160228_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspections',
            name='facility_guid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
