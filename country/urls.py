from django.conf.urls import url
from .views import CountryView


urlpatterns = [

    url(r'pais/$', CountryView.as_view(), name='country'),
    #url(r'^verificar-inscripcion/$', VerifySignUpActivity.as_view(), name='verify-sign-up-activity'),
    #url(r'^asistencia/$', VerifySignUpActivity.as_view(),name='activities'),
]