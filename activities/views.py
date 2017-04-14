from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from .models import SignUpActivities, Activities
from datetime import datetime
from profiles.models import IdCard
from topics.models import ActivityRoom
from .forms import VerifySignUpForm
from agenda.models import TopicAgenda
from rooms.models import Room
from agenda.models import Agenda, SignUpSchedule
from django.contrib.auth.mixins import LoginRequiredMixin
import threading


class ActivitiesView(LoginRequiredMixin, TemplateView):
    template_name = 'activities/list-activity.html'
    class_form = ""
    login_url = "/iniciar-sesion"

    def get(self, request, *args, **kwargs):
        if "load" in request.GET:
           
            state = "init"
            response_data = {}
            message = ""
            is_error = False
            activity_list = []
            count = 0

            try:

                state = "get info"

                obj_activities = Activities.objects.filter(active=True)
                
                for ix_act, val_act in enumerate(obj_activities):

                    list = {}

                    list['id_html'] = count + 1
                    list['activity_code'] = val_act.activities_code
                    list['begin_date'] = str(val_act.begin_date)
                    list['finish_date'] = str(val_act.finish_date)
                    list['topic'] = val_act.topic
                    list['is_pay'] = val_act.is_pay
                    list['description'] = val_act.description
                    activity_list.append(list)
                    count = count +1
                count = 0

                state = "finish"    
            except Exception as e:

                is_error = True
                message = "error en el sistema por favor comuniquese con soporte"
                response_data['type_error'] = type(e).__name__
                response_data['file'] = "activities view"
                response_data['class'] = "ActivitiesView"
                response_data['state'] = state

            response_data['message'] = message
            response_data['is_error'] = is_error
            response_data['activity_list'] = activity_list
            response_json = json.dumps(response_data)
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)

        else:

            dic = {}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        try:

            authenticated = False
            response_data = {}
            message = ""
            is_error = False
            user = request.user

            state = "init"
            if user.is_authenticated():
                authenticated = True
                
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                obj_activity = Activities.objects.filter(activities_code=body['activity_code'], active=True)
                obj_sign_up_activities = SignUpActivities.objects.filter(fk_activities=obj_activity,
                                                                        fk_user=user,
                                                                        active=True)
                state = "validate"
                if obj_sign_up_activities:
                    message = "ya estas inscrito en la actividad"

                else:

                    state = "sign up"
                    obj_sign_up_activities = SignUpActivities()
                    obj_sign_up_activities.create(obj_activity[0], request.user)

                    """
                    obj_id_card = IdCard()
                    obj_id_card.created_at = datetime.today()
                    obj_id_card.fk_user_created = request.user
                    obj_id_card.fk_sign_activity_code = sign_up_code
                    obj_id_card.save()

                    """
                    message = "Gracias por inscribirte en nuestra actividad"

            else:
                message = "por favor inicie sesion para regitrarte en la actividad"

            state ="finish"

        except Exception as e:

            print str(e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
        

class VerifySignUpActivity(LoginRequiredMixin,TemplateView):

    template_name = "activities/verify-sign-up-activity.html"
    form_class = VerifySignUpForm()
    login_url = "/index/"

    def get(self,request,*args,**kwargs):

        response_data = {}
        is_error = False
        exist = False
        lock = threading.Lock()
        lock.acquire()
        if 'sign_up_code' in request.GET:

            try:

                sign_up_code = request.GET['sign_up_code']
                activity_id = request.GET['activity_id']
                room_id = request.GET['room_id']
                agenda_id = request.GET['agenda_id']

                obj_room = Room.objects.filter(pk = room_id)
                room_code = obj_room[0].room_code

                obj_activities = Activities.objects.filter(pk = activity_id)
                activities_code = obj_activities[0].activities_code

                obj_agenda = Agenda.objects.filter(pk = agenda_id)
                agenda_code = obj_agenda[0].agenda_code

                obj_activity_room = ActivityRoom.objects.filter(active = True, fk_room_code = room_code, fk_activity_code = activities_code)
                if(obj_activity_room):

                    for index,valActRoom in enumerate(obj_activity_room):

                        activity_room_code = valActRoom.activity_room_code
                        obj_topic_agenda = TopicAgenda.objects.filter(active = True, fk_agenda_code = agenda_code, fk_activity_room_code = activity_room_code)
                        if(obj_topic_agenda):

                            topic_agenda_code = obj_topic_agenda[0].topic_agenda_code
                            obj_sign_up_schedule = SignUpSchedule.objects.filter(action = True , fk_sign_up_code = sign_up_code, fk_topic_agenda = topic_agenda_code)

                            if(obj_sign_up_schedule):

                                message = "el asistente ha separado cupo para este evento"

                            else:

                                message = "el asistente no ha separado cupo para este evento"


            except Exception as e:

                is_error = True
                message = "error en el sistema por favor comuniquese con soporte"
                response_data['type_error'] = type(e).__name__

        else:

            dic = {'form':self.form_class}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
        lock.release()
