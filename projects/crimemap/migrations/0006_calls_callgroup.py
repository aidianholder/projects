# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-29 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimemap', '0005_auto_20160507_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='callgroup',
            field=models.CharField(default='OT', max_length=2),
            preserve_default=False,
        ),
    ]
