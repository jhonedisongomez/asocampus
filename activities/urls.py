from django.conf.urls import url
from .views import ActivitiesView, VerifySignUpActivity


urlpatterns = [

    url(r'^activities/$', ActivitiesView.as_view(),name='activities'),
    url(r'^verificar-inscripcion/$', VerifySignUpActivity.as_view(),name='verify-sign-up-activity'),
    #url(r'^asistencia/$', VerifySignUpActivity.as_view(),name='activities'),
]
