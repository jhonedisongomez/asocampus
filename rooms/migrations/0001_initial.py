# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-07-31 22:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(db_index=True, max_length=30)),
                ('table', models.CharField(db_index=True, max_length=20)),
                ('field', models.CharField(db_index=True, max_length=20)),
                ('before_value', models.CharField(db_index=True, max_length=30)),
                ('after_value', models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ('date', models.DateField(db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auditor_room_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(db_index=True, default=uuid.uuid4, max_length=64)),
                ('room_name', models.CharField(blank=True, max_length=40, null=True)),
                ('address', models.CharField(blank=True, max_length=40, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('fk_section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.Section')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='room',
            index_together=set([('room_code', 'active')]),
        ),
        migrations.AlterIndexTogether(
            name='auditorroom',
            index_together=set([('action', 'table', 'field', 'before_value', 'after_value', 'date')]),
        ),
    ]
