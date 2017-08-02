# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-08-01 13:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorRol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(db_index=True, max_length=30)),
                ('table', models.CharField(db_index=True, max_length=20)),
                ('field', models.CharField(db_index=True, max_length=20)),
                ('before_value', models.CharField(db_index=True, max_length=30)),
                ('after_value', models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ('date', models.DateField(db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auditor_rol_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles_code', models.CharField(blank=True, db_index=True, default=uuid.uuid4, max_length=64)),
                ('roles_name', models.CharField(max_length=64)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('version', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RolesProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol_profile_code', models.CharField(blank=True, db_index=True, default=uuid.uuid4, max_length=64)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('version', models.IntegerField()),
                ('fk_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles_profile', to='profiles.Profile')),
                ('fk_rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles_profile', to='roles.Roles')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='roles',
            index_together=set([('roles_code', 'active')]),
        ),
        migrations.AlterIndexTogether(
            name='auditorrol',
            index_together=set([('action', 'table', 'field', 'before_value', 'after_value', 'date')]),
        ),
    ]
