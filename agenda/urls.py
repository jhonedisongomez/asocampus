from django.conf.urls import url
from .views import AgendaView, CreateDateView, CreateAgendaView, ListScheduleView

urlpatterns = [

    url(r'^lista-de-actividades/$', AgendaView.as_view(),name='activity_list'),
    url(r'crear-fecha/$', CreateDateView.as_view(),name='create-date'),
    url(r'crear-agenda/$', CreateAgendaView.as_view(),name='create-agenda'),
    url(r'list-schedule/$', ListScheduleView.as_view(),name='list-schedule'),

]
