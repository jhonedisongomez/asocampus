from django.conf.urls import url
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^$', SignIn.as_view(), name='sign-in'),

    # url(r'^inicia-sesion/$', 'django.contrib.auth.views.login', {'template_name': 'users/sign-in.html'}, name='login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

]
