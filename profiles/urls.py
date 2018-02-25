from django.conf.urls import url
from .views import ProfileView

urlpatterns = [
    url(r'^mi-perfil/$', ProfileView.as_view(), name='my-profile'),

]
