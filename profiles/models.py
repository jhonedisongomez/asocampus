from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
from activities.models import SignUpActivities


class IdType(models.Model):

    id_type_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    description = models.CharField(max_length=30,blank=False,null=True)
    active = models.BooleanField(default=True, null=False, blank=True, db_index=True)

    class Meta:
        index_together =(
            ('id_type_code', 'active')
        )


class Profile(models.Model):

    profile_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    document_id = models.IntegerField(max_length=11, db_index=True, blank=False, null=False)
    first_name = models.CharField(max_length=20, db_index=True, blank=False, null=False)
    last_name = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    mobil_number = models.CharField(max_length=11,blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    version = models.IntegerField(default=0,blank=False, null=True)
    fk_id_type = models.ForeignKey(IdType)
    fk_user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        index_together = (
            ('profile_code', 'active'),
            ('active', 'fk_user'),
            ('document_id', 'active', 'fk_user')

        )

    def __unicode__(self):
        return self.first_name + self.last_name


class IdCard(models.Model):

    id_card_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    is_downloaded = models.BooleanField(default=False)
    fk_sign_activity_code = models.ForeignKey(SignUpActivities)


class AuditorProfile(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    table = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    field = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    before_value = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    after_value = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    date = models.DateField(null=False, blank=False, db_index=True)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_profile_user')

    class Meta:
        index_together = (
            ('action', 'table', 'field', 'before_value', 'after_value', 'date')

        )
