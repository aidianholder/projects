# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-07 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimemap', '0003_auto_20160507_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='calldatetime',
            field=models.DateTimeField()
        ),
    ]
