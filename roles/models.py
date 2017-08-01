from __future__ import unicode_literals
import uuid
from django.db import models
from country.models import Country
from profiles.models import Profile
from activities.models import Activities
from django.contrib.auth.models import User


class Roles(models.Model):
    roles_code = models.CharField(max_length=64, default=uuid.uuid4, null=False, blank=True, db_index=True)
    roles_name = models.CharField(max_length=64, null=False, blank=False)
    active = models.BooleanField(default=True, db_index=True)
    version = models.IntegerField(blank=False, null=False)

    class Meta:
        index_together = (
        ('roles_code', 'active')

    )

    def __unicode__(self):
    
        return self.roles_name


class RolesProfile(models.Model):
    rol_profile_code = models.CharField(max_length=64, default=uuid.uuid4, null=False, blank=True, db_index=True)
    fk_profile = models.ForeignKey(Profile, blank=False, null=True, related_name='roles_profile')
    fk_rol = models.ForeignKey(Roles, blank=False, null=True, related_name='roles_profile')
    active = models.BooleanField(default=True, db_index=True)
    version = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        
        return self.rol_profile_code


class ProfileRolActivity(models.Model):
    ProfileRolActivity = models.CharField(max_length=64, default=uuid.uuid4, null=False, blank=True, db_index=True)
    fk_rol_profile = models.ForeignKey(RolesProfile, blank=False, null=True, related_name='roles_profile_activity')
    fk_activity = models.ForeignKey(Activities, blank=False, null=True, related_name='roles_profile_activity')
    active = models.BooleanField(default=True, db_index=True)
    version = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
            
        return self.ProfileRolActivity


class AuditorRol(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    table = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    field = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    before_value = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    after_value = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    date = models.DateField(null=False, blank=False, db_index=True)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_rol_user')

    class Meta:
        index_together = (
            ('action', 'table', 'field', 'before_value', 'after_value', 'date')

        )