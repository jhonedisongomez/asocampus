from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from country.models import Section


class ActivitiesType(models.Model):
    activities_type_Code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    description = models.CharField(max_length=30, blank=False)
    active = models.BooleanField(default=True, blank=False, db_index=True)

    def __unicode__(self):

        return self.description


class Activities(models.Model):
    activities_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    begin_date = models.DateField(blank=False, null=False)
    finish_date = models.DateField(blank=False, null=False)
    topic = models.CharField(max_length=200, blank=False, null=False)
    active = models.BooleanField(default=True, db_index=True)
    isPaid = models.BooleanField(default=False, db_index=True)  # to know if the activity as a price
    fk_activities_type = models.ForeignKey(ActivitiesType, blank=False, null=False)
    fk_section = models.ForeignKey(Section)

    class Meta:
        index_together = (
            ('activities_code', 'begin_date', 'active', 'isPaid')

        )

    def __unicode__(self):
        return self.topic


class SignUpActivities(models.Model):
    sign_up_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True)
    fk_activities = models.ForeignKey(Activities)
    fk_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.fk_user.username


class AuditorTopic(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_activities_user')