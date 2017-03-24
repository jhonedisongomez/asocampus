from django.conf.urls import url, include
from .views import SignInView, SignUpView


urlpatterns = [
    url(r'^iniciar-sesion/$', SignInView.as_view(), name='login'),
    url(r'^registro/$', SignUpView.as_view(), name='signUp'),
]
