from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from rooms.models import Room
from activities.models import Activities


class Topic(models.Model):
    topic_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    topic_name = models.CharField(max_length=40, blank=True, null=True)
    professor_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)

    def __unicode__(self):
        return self.topic_name


class ActivityRoom(models.Model):
    activity_room_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    fk_room = models.ForeignKey(Room)
    fk_activity = models.ForeignKey(Activities)
    fk_topic = models.ForeignKey(Topic)

    def __unicode__(self):

        obj_activity = Activities.objects.filter(activities_code = self.fk_activity_code, active = True)
        if obj_activity:
            activity = obj_activity[0].thopic

            obj_room = Room.objects.filter(room_code = self.fk_room_code,active = True)
            room_name = obj_room[0].room_name

            obj_topic = Topic.objects.filter(topic_code = self.fk_topic_code,active = True)
            topic_name = obj_topic[0].topic_name
            return activity + " - " + topic_name + " - " + room_name
        else:

            return self.activity_room_code


class AuditorTopic(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_topic_user')
