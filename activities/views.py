from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from .models import SignUpActivities, Activities, AuditorActivity
from topics.models import ActivityRoom
from .forms import VerifySignUpForm
from agenda.models import TopicAgenda
from rooms.models import Room
from agenda.models import Agenda, SignUpSchedule
from django.contrib.auth.mixins import LoginRequiredMixin
import threading
import logging


logger = logging.getLogger("logging")

class ActivitiesView(LoginRequiredMixin, TemplateView):

    template_name = 'activities/list-activity.html'
    class_form = ""
    login_url = "/"

    def get(self, request, *args, **kwargs):
        logger.info(str(request) +  ", usuario:" +  str(request.user))

        if "load" in request.GET:
            print (str(request))
            state = "init"
            logger.info("state: " + state + ", usuario:" + str(request.user))
            response_data = {}
            message = ""
            is_error = False
            activity_list = []
            count = 0

            try:

                state = "get info"
                logger.info("state: " + state + ", usuario:" + str(request.user))
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

                logger.error(e)
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
            logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)

        else:

            dic = {}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        created = False
        counter = ""

        try:

            user = request.user
            state = "init"
            logger.info("state: " + state + ", usuario:" + str(request.user))
            if user.is_authenticated():

                logger.info(str(request.body.decode('utf-8')) +  ", usuario:" +  str(request.user))
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                obj_activity = Activities.objects.filter(activities_code=body['activity_code'], active=True)
                obj_sign_up_activities = SignUpActivities.objects.filter(active=True,
                                                                         fk_activities=obj_activity,
                                                                        fk_user=user)
                state = "validate"
                logger.info("state: " + state + ", usuario:" + str(request.user))
                if obj_sign_up_activities:
                    message = "ya estas inscrito en la actividad"

                else:
                    obj_sign_up_activities = SignUpActivities.objects.filter(active=True,
                                                     fk_activities=obj_activity)

                    state = "validate limit"
                    logger.info("state: " + state + ", usuario:" + str(request.user))
                    if obj_sign_up_activities:

                        obj_sign_up_activities = SignUpActivities.objects.filter(active=True,
                                                         fk_activities=obj_activity).order_by('-id')[0]

                        counter = obj_sign_up_activities.count + 1

                    else:
                        counter = 1

                    if counter <= obj_activity[0].limit:

                        created = True
                        state = "sign up"
                        logger.info("state: " + state + ", usuario:" + str(request.user))
                        obj_sign_up_activities = SignUpActivities()
                        obj_sign_up_activities.count = counter
                        obj_sign_up_activities.fk_activities = obj_activity[0]
                        obj_sign_up_activities.fk_user = request.user

                        obj_auditor_topic = AuditorActivity()
                        obj_auditor_topic.action = "SAVE"
                        obj_auditor_topic.table = "SignUpActivities"
                        obj_auditor_topic.field = "ALL"
                        obj_auditor_topic.after_value = str(obj_sign_up_activities.sign_up_code) + "," + str(obj_sign_up_activities.active) + "," + str(obj_activity[0].pk) + ","\
                                                                                                        + str(request.user.pk)
                        obj_auditor_topic.user = request.user

                        message = "Gracias por inscribirte en nuestra actividad"

                    else:

                        message = "esta actividad ya no tiene cupo disponible"

            else:
                message = "por favor inicie sesion para regitrarte en la actividad"

            state ="finish"
            logger.info("state: " + state + ", usuario:" + str(request.user))

        except Exception as e:

            print str(e)
            logger.error(e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state


        else:
            if created:

                obj_sign_up_activities.save()
                obj_auditor_topic.save()
                state = "save"
                logger.info("state: " + state + ", usuario:" + str(request.user))

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
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
