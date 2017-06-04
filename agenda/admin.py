from django.contrib import admin

from .models import Agenda, SignUpSchedule,TopicAgenda

admin.site.register(Agenda)
admin.site.register(SignUpSchedule)
admin.site.register(TopicAgenda)
