from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    country_code = models.CharField(max_length=64, default=uuid.uuid4, null=False, blank=True, db_index=True)
    country_name = models.CharField(max_length=64, null=False, blank=False)
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        index_together = (
            ('country_code', 'active')

        )

    def __unicode__(self):

        return self.country_name


class SectionType(models.Model):
    section_type_code = models.CharField(max_length=64, default=uuid.uuid4, blank=False, null=True, db_index=True)
    section_type_name = models.CharField(max_length=40, blank=False, null=True)
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        index_together = (
            ('section_type_code', 'active')

        )

    def __unicode__(self):

        return self.section_type_name


class Section(models.Model):
    section_code = models.CharField(max_length=64, default=uuid.uuid4, blank=False, null=True, db_index=True)
    section_name = models.CharField(max_length=30, blank=False, null=False)
    active = models.BooleanField(default=True, db_index=True)
    fk_country = models.ForeignKey(Country, blank=False, null=True, related_name='section_country')
    fk_section = models.ForeignKey('self', blank=True, null=True, related_name='section_section')
    fk_section_type = models.ForeignKey(SectionType, blank=False, null=True, related_name='section_section_type')

    class Meta:
        index_together = (
            ('section_code', 'active')

        )

    def __unicode__(self):

        return self.section_name


class AuditorCountry(models.Model):
    action = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    table = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    field = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    before_value = models.CharField(max_length=30, blank=False, null=False, db_index=True)
    after_value = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    date = models.DateField(null=False, blank=False, db_index=True)
    user = models.ForeignKey(User, blank=False, null=False, related_name='auditor_country_user')

    class Meta:
        index_together = (
            ('action', 'table', 'field', 'before_value', 'after_value', 'date')

        )