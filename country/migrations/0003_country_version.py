# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-08-27 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0002_auto_20170827_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='version',
            field=models.IntegerField(null=True),
        ),
    ]
