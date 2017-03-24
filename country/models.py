from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    country_code = models.CharField(max_length=64, default=uuid.uuid4, null=False, blank=True)
    country_name = models.CharField(max_length=64, null=False, blank=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):

        return self.country_name


class SectionType(models.Model):
    section_type_code = models.CharField(max_length=64, default=uuid.uuid4, blank=False, null=True)
    section_type_name = models.CharField(max_length=40, blank=False, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):

        return self.section_type_name


class Section(models.Model):
    section_code = models.CharField(max_length=64, default=uuid.uuid4, blank=False, null=True)
    section_name = models.CharField(max_length=30, blank=False, null=False)
    active = models.BooleanField(default=True)
    fk_country = models.ForeignKey(Country, blank=False, null=True, related_name='section_country')
    fk_section = models.ForeignKey('self', related_name='section_section')
    fk_section_type = models.ForeignKey(SectionType, blank=False, null=True, related_name='section_section_type')

    def __unicode__(self):

        return self.section_name


class AuditorCountry(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False)
    table = models.CharField(max_length=20, blank=False, null=False)
    field = models.CharField(max_length=20, blank=False, null=False)
    before_value = models.CharField(max_length=30, blank=False, null=False)
    after_value = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_country_user')