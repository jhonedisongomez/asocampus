from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from topics.models import Topic, ActivityRoom
from rooms.models import Room
from activities.models import Activities, SignUpActivities


class Agenda(models.Model):

    agenda_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    schedule = models.CharField(max_length=20, blank=False, null=False)
    date = models.DateField()
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        index_together = (
            ('agenda_code', 'date', 'active')

        )

    def __unicode__(self):
        return str(self.date) + " - " + self.schedule


class TopicAgenda(models.Model):

    topic_agenda_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    fk_agenda = models.ForeignKey(Agenda)
    fk_activity_room = models.ForeignKey(ActivityRoom)

    class Meta:
        index_together = (
            ('topic_agenda_code', 'active')

        )

    def __unicode__(self):

        obj_agenda = Agenda.objects.filter(pk=self.fk_agenda.pk)
        schedule = obj_agenda[0].schedule
        date = obj_agenda[0].date

        obj_activity_room = ActivityRoom.objects.filter(pk=self.fk_activity_room.pk)
        room_pk = obj_activity_room[0].fk_room.pk
        topic_pk = obj_activity_room[0].fk_topic.pk
        activity_pk = obj_activity_room[0].fk_activity.pk

        obj_activity = Activities.objects.filter(pk=activity_pk)
        activity = obj_activity[0].topic

        obj_room = Room.objects.filter(pk=room_pk)
        room_name = obj_room[0].room_name

        obj_topic = Topic.objects.filter(pk=topic_pk)
        topic_name = obj_topic[0].topic_name

        return activity + " - " + str(date) + " - " + schedule + " - " + room_name + " - " + topic_name


class SignUpSchedule(models.Model):

    sign_up_schedule_code = models.CharField(max_length=64, default=uuid.uuid4,
                            db_index=True)
                            
    count = models.CharField(max_length=2000, blank=False, null=False)
    action = models.BooleanField(default=True, db_index=True)
    fk_sign_up_code = models.ForeignKey(SignUpActivities)
    fk_topic_agenda = models.ForeignKey(TopicAgenda)

    class Meta:
        index_together = (
            ('sign_up_schedule_code', 'action')

        )

class AuditorAgenda(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    table = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    field = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    before_value = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    after_value = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    date = models.DateField(null=False, blank=False, db_index=True)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_agenda_user')

    class Meta:
        index_together = (
            ('action', 'table', 'field', 'before_value', 'after_value', 'date')

        )
