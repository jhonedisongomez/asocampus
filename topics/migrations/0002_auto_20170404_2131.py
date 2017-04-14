# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-04-05 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditortopic',
            name='action',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='auditortopic',
            name='after_value',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='auditortopic',
            name='before_value',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='auditortopic',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='auditortopic',
            name='field',
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='auditortopic',
            name='table',
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.AlterIndexTogether(
            name='activityroom',
            index_together=set([('activity_room_code', 'active')]),
        ),
        migrations.AlterIndexTogether(
            name='auditortopic',
            index_together=set([('action', 'table', 'field', 'before_value', 'after_value', 'date')]),
        ),
        migrations.AlterIndexTogether(
            name='topic',
            index_together=set([('topic_code', 'active')]),
        ),
    ]
