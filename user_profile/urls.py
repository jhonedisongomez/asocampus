from django.conf.urls import url, include
from .views import SignInView, SignUpView, Logout


urlpatterns = [
    url(r'^iniciar-sesion/$', SignInView.as_view(), name='login'),
    url(r'^cerrar-sesion/$', Logout.as_view(), name='logout'),
    url(r'^registro/$', SignUpView.as_view(), name='signUp'),
]
