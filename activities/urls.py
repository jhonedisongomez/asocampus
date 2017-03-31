from django.conf.urls import url
from .views import ActivitiesView, VerifySignUpActivity


urlpatterns = [

    # url(r'^lista-de-actividades/$', AgendaView.as_view(),name='activity_list'),
    url(r'^lista-de-actividades/$', ActivitiesView.as_view(), name='activity_list'),
    url(r'^verificar-inscripcion/$', VerifySignUpActivity.as_view(), name='verify-sign-up-activity'),
    #url(r'^asistencia/$', VerifySignUpActivity.as_view(),name='activities'),
]
