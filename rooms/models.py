from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from country.models import Section


class Room(models.Model):

    room_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    room_name = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    fk_section = models.ForeignKey(Section, blank=True, null=True)

    def __unicode__(self):
        return self.room_name


class AuditorRoom(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_room_user')
