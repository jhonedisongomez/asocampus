# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2018-01-08 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20171007_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='image_location',
            field=models.ImageField(blank=True, upload_to='activity_image'),
        ),
    ]
