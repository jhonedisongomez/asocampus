# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-08-28 02:31
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0005_auto_20170827_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='country_code',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=64),
        ),
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterIndexTogether(
            name='country',
            index_together=set([('country_name', 'active')]),
        ),
    ]