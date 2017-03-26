from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from topics.models import Topic, ActivityRoom
from rooms.models import Room
from activities.models import Activities

class Agenda(models.Model):

    agenda_code = models.CharField(max_length = 64, default = uuid.uuid4)
    schedule = models.CharField(max_length = 20, blank = False, null = False)
    date = models.DateField()
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now = True,blank = False)
    fk_user_created = models.ForeignKey(User,related_name ='agenda_creator')
    modified_at = models.DateTimeField(null = True, blank = True)
    fk_user_modified = models.ForeignKey(User, null = True,blank = True, related_name = 'agenda_updater')

    def __unicode__(self):
        return str(self.date) +" - " + self.schedule

class SignUpSchedule(models.Model):

    sign_up_schedule_code = models.CharField(max_length = 64, default = uuid.uuid4)
    count = models.CharField(max_length = 2000,blank = False, null = False)
    action = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now = True,blank = False)
    fk_user_created = models.ForeignKey(User,related_name ='sign_up_schedule_creator')
    fk_sign_up_code = models.CharField(max_length = 64)
    fk_topic_agenda = models.CharField(max_length = 64)


class TopicAgenda(models.Model):

    topic_agenda_code = models.CharField(max_length = 64, default = uuid.uuid4)
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now = True,blank = False)
    fk_user_created = models.ForeignKey(User,related_name ='topic_agenda_creator')
    modified_at = models.DateTimeField(null = True, blank = True)
    fk_user_modified = models.ForeignKey(User, null = True,blank = True, related_name = 'topic_agenda_updater')
    fk_agenda_code = models.CharField(max_length = 64)
    fk_activity_room_code = models.CharField(max_length = 64)

    def __unicode__(self):

        obj_agenda = Agenda.objects.filter(agenda_code = self.fk_agenda_code, active = True)
        schedule = obj_agenda[0].schedule
        date = obj_agenda[0].date

        obj_activity_room = ActivityRoom.objects.filter(activity_room_code = self.fk_activity_room_code, active = True)
        room_code = obj_activity_room[0].fk_room_code
        topic_code = obj_activity_room[0].fk_topic_code
        activity_code = obj_activity_room[0].fk_activity_code

        obj_activity = Activities.objects.filter(activities_code =  activity_code,active = True)
        activity = obj_activity[0].thopic

        obj_room = Room.objects.filter(room_code = room_code, active = True)
        room_name  = obj_room[0].room_name

        obj_topic = Topic.objects.filter(topic_code = topic_code,active = True)
        topic_name = obj_topic[0].topic_name

        return activity + " - " + str(date) + " - " + schedule + " - " + room_name + " - " + topic_name
