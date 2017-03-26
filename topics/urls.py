from django.conf.urls import url
from .views import CreateActivity, CreateTopicView


urlpatterns = [

    url(r'^crear-actividad-por-tema/$', CreateActivity.as_view(),name='create-activity-thopic'),
    url(r'^crear-tema/$', CreateTopicView.as_view(),name='create-topic'),



]
