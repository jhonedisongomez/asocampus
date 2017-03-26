from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
from activities.models import SignUpActivities


class IdCard(models.Model):

    id_card_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    is_downloaded = models.BooleanField(default=False)
    fk_sign_activity_code = models.ForeignKey(SignUpActivities)


class AuditorProfile(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_profile_user')
