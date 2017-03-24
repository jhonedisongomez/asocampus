from django.conf.urls import url
from .views import ListRoomView, CreateRoomView

urlpatterns = [

    url(r'^list-rooms/$', ListRoomView.as_view(),name='list_rooms'),
    url(r'^crear-salon/$', CreateRoomView.as_view(),name='create-room'),

]
