from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
from activities.models import Activities


class Payment(models.Model):

    payment_code = models.CharField(max_length=64, default=uuid.uuid4, db_index=True)
    price = models.IntegerField(blank=False, null=False)
    active = models.BooleanField(default=True, db_index=True)
    fk_activity = models.ForeignKey(Activities)


# model to know if a person is pay the activity


class PaymentPerson(models.Model):

    payment_person_code = models.CharField(max_length=64, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True, blank=False)
    fk_user_created = models.ForeignKey(User, related_name='payment_person_creator')
    fk_payment = models.ForeignKey(Payment)
    fk_user_pay = models.ForeignKey(User, null=True, blank=True, related_name='payment_buyer')


class AuditorPayment(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_payment_user')
