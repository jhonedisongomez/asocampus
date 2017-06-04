from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from .models import Room
from country.models import section
from .forms import ListMunicipio

class ListRoomView(LoginRequiredMixin, TemplateView):

    template_name = "activities/verify-sign-up-activity.html"
    form_class = ""
    #login_url = "/"

    def get(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        room_list = []

        try:

            section_pk = request.GET['section']
            obj_section = section.objects.filter(pk = section_pk)
            section_code = obj_section[0].section_code

            obj_room = Room.objects.filter(active = True,fk_section_code = section_code)
            if(obj_room):

                for index,valRoom in enumerate(obj_room):
                    room_data = {}
                    room_name = valRoom.room_name
                    room_pk = valRoom.pk

                    room_data['room_name'] = room_name
                    room_data['room_pk'] = room_pk

                    room_list.append(room_data)
        except Exception as e:

            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__

        response_data['message'] = message
        response_data['is_error'] = is_error
        response_data['rooms_list'] = room_list

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)

        return response_data

class CreateRoomView(LoginRequiredMixin, TemplateView):

    template_name = "rooms/create-room.html"
    #login_url = "/"
    form_class = ListMunicipio()

    def get(self, request, *args, **kwargs):

        dic = {'form':self.form_class}
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        try:

            response_data = {}
            message = ""
            is_error = False

            user = request.user
            room_name = request.POST['room_name']
            address = request.POST['address']
            capacity = request.POST['capacity']

            section_pk = request.POST['section']
            obj_section = section.objects.filter(pk = section_pk)
            section_code = obj_section[0].section_code

            obj_room = Room()
            obj_room.room_name = room_name
            obj_room.address = address
            obj_room.capacity = capacity
            obj_room.fk_user_created = user
            obj_room.fk_section_code = section_code
            obj_room.save()

            message = "se ha creado un nuevo salon"

        except Exception as e:

            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
