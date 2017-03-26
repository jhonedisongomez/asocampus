from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from .models import ActivityRoom, Topic
from .forms import CreateActivityRoomForm
from rooms.models import Room
from activities.models import Activities

class CreateActivity(TemplateView, LoginRequiredMixin):

    template_name = "activities/create-activity.html"
    #login_url = "/"
    form_class = CreateActivityRoomForm()

    def get(self, request, *args, **kwargs):

        dic = {'form': self.form_class}
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        try:

            #get the data from the templates
            room_pk = request.POST['room']
            activity_pk = request.POST['activity']
            topic_pk = request.POST['topic']

            obj_room = Room.objects.filter(pk = room_pk)
            room_code = obj_room[0].room_code

            obj_activity = Activities.objects.filter(pk = activity_pk)
            activity_code = obj_activity[0].activities_code

            obj_topic = Topic.objects.filter(pk = topic_pk)
            topic_code = obj_topic[0].topic_code

            obj_activity_room_search = ActivityRoom.objects.filter(active = True,fk_room_code = room_code, fk_activity_code = activity_code, fk_topic_code = topic_code)

            if obj_activity_room_search:
                message = "este tema ya existe con este evento y salon, por favor cree uno nuevo"
            else:

                user = request.user
                obj_activity_room = ActivityRoom()
                obj_activity_room.fk_user_created = user
                obj_activity_room.fk_room_code = room_code
                obj_activity_room.fk_activity_code = activity_code
                obj_activity_room.fk_topic_code = topic_code
                obj_activity_room.save()

                message = "se ha creado un nuevo registro en la base de datos"
        except Exception as e:

            is_error = True
            message = "error en reservar cupo, por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)


class CreateTopicView(LoginRequiredMixin, TemplateView):

    template_name = "topics/create-topic.html"
    #login_url = "/index/"

    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False

        topic_name = request.POST['topic_name']
        professor_name = request.POST['professor_name']
        description = request.POST['description']
        user = request.user
        obj_topic = Topic()
        obj_topic.topic_name = topic_name
        obj_topic.profesor_name = professor_name
        obj_topic.description = description
        obj_topic.fk_user_created = user
        obj_topic.save()

        message = "se ha guardado un tema en la base de datos"


        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
