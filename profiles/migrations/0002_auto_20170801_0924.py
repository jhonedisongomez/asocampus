# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-08-01 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='document_id',
            field=models.IntegerField(blank=True, db_index=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fk_id_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.IdType'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]