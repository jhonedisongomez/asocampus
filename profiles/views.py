# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, IdType, AuditorProfile
import logging
from datetime import datetime
from django.contrib.auth.models import User
from django.db import connection

logger = logging.getLogger("logging")


class ProfileView(TemplateView):

    template_name = "profile/profile.html"
    class_form = ""
    login_url = "/"

    def get(self, request, *args, **kwargs):

        state = "init"
        logger.info("state: " + state + ", usuario:" + str(request.user))
        response_data = {}
        profile_data = {}
        data = []
        message = ""
        is_error = False

        if "load" in request.GET:
            try:

                profile = None
                state = "init profile"
                logger.info("state: " + state + ", usuario:" + str(request.user))
                
                with connection.cursor() as cursor:

                    cursor.callproc('get_profile_activity',[request.user.id])
                    profile = cursor.fetchone()

                if(profile[0] is False):
                   
                    profile_data['document_id'] = profile[3]
                    profile_data['first_name'] = profile[4]
                    profile_data['last_name'] = profile[5]
                    profile_data['name'] = profile[4] + " " + profile[5]
                    profile_data['phone_number'] = profile[6]
                    profile_data['mobil_number'] = profile[7]
                    profile_data['email'] = request.user.email
                    data.append(profile_data)
                    response_data['data'] = data

                    state = "finish get profile"
                    logger.info("state: " + state + ", usuario:" + str(request.user))

                else:

                    message = profile[1]
                    is_error = True
                    
            except Exception as e:
                
                logger.error(e)
                is_error = True
                message = "error en el sistema por favor comuniquese con soporte"
                response_data['type_error'] = type(e).__name__
                response_data['file'] = "profile view"
                response_data['class'] = "ProfileView"
                response_data['state'] = state

            response_data['message'] = message
            response_data['is_error'] = is_error

            response_json = json.dumps(response_data)
            logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)

        else:
            dic = {}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance) 

    def post (self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        created = False
        edited = False
        state = "init"

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        method = body['method']
        logger.info("state: " + state + ",profileView,post" + str(body) + ", usuario:" + str(request.user))

        try:

            if method == "create":
                created = True
                edited = False
                state = "init create"
                logger.info("state: " + state + ", usuario:" + str(request.user))
                obj_id_type = IdType.objects.filter(pk=body['id_type'])
                obj_user = User.objects.filter(email = body['email'])

                obj_profile = Profile()
                obj_profile.document_id = body['id']
                obj_profile.first_name = body['first_name']
                obj_profile.last_name = body['last_name']
                obj_profile.phone_number = body['phone_number']
                obj_profile.mobil_number = body['mobil_number']
                obj_id_type = IdType.objects.filter(pk = body['id_type'])

                obj_profile.fk_id_type = obj_id_type[0]
                obj_profile.fk_user = obj_user[0]

                obj_auditor_profile = AuditorProfile()
                obj_auditor_profile.action = "CREATE"
                obj_auditor_profile.table = "Profile"
                obj_auditor_profile.field = "ALL"
                obj_auditor_profile.after_value = str(obj_profile.profile_code) + "," + str(obj_profile.document_id) +"," \
                + str(obj_profile.first_name) + "," + str(obj_profile.last_name) + "," + str(obj_profile.phone_number) + "+" \
                + str(obj_profile.mobil_number) + "," + str(obj_profile.active) + "," + str(obj_profile.fk_id_type) + "," \
                + str(obj_user[0].pk)
                obj_auditor_profile.date = datetime.today()
                obj_auditor_profile.user = obj_user[0]

                #message = "Su perfil ha sido guardado en la base de datos"
                state = "finish create"
                logger.info("state: " + state + ", usuario:" + str(request.user))

            if method == "edit":
                state = "init edit"
                logger.info("state: " + state + ", usuario:" + str(request.user))

                obj_profile1 = Profile.objects.filter(active = True, fk_user = request.user)
                obj_profile1[0].active = False

                obj_profile2 = Profile()
                obj_profile2.profile_code = obj_profile1[0].profile_code
                obj_profile2.document_id = body['document_id']
                obj_profile2.first_name = body['first_name']
                obj_profile2.last_name = body['last_name']
                if(body['phone_number'] != ""):

                    obj_profile2.phone_number = int(body['phone_number'])

                obj_profile2.mobil_number = body['mobil_number']
                obj_profile2.active = True
                obj_profile2.version = obj_profile1[0].version + 1

                id_type = IdType.objects.filter(pk=body['id_type'], active=True)

                obj_profile2.fk_id_type = id_type[0]
                obj_profile2.fk_user = request.user
                state = "compare edit"
                logger.info("state: " + state + ", usuario:" + str(request.user))
                if obj_profile1[0] != obj_profile2:

                    state = "diferent profile"
                    logger.info("state: " + state + ", usuario:" + str(request.user))
                    fields = ""
                    values = ""
                    old_values = ""
                    state = "init auditory edit"
                    logger.info("state: " + state + ", usuario:" + str(request.user))
                    obj_auditor_profile = AuditorProfile()
                    obj_auditor_profile.action = "EDIT"
                    obj_auditor_profile.table = "Profile"

                    if obj_profile1[0].document_id != obj_profile2.document_id:

                        fields = "document_id"
                        values = str(obj_profile2.document_id)
                        old_values = str(obj_profile1[0].document_id)

                    if obj_profile1[0].first_name != obj_profile2.first_name:
                        old_values = old_values+ "," + obj_profile1[0].first_name
                        if fields != "":
                            fields = fields + ",first name"
                            values = values +"," + obj_profile2.first_name
                        else:
                            fields = "first name"
                            values = obj_profile2.first_name

                    if obj_profile1[0].last_name != obj_profile2.last_name:
                        old_values = old_values +"," + obj_profile1[0].last_name

                        if fields != "":
                            fields = fields + ",last name"
                            values = values +"," + obj_profile2.last_name
                        else:
                            fields = "last name"
                            values = obj_profile2.last_name

                    if obj_profile1[0].phone_number != obj_profile2.phone_number:
                        old_values = old_values + "," + str(obj_profile1[0].phone_number)
                        if fields != "":
                            fields = fields + ",phone number"
                            values = values +"," + str(obj_profile2.phone_number)
                        else:
                            fields = "phone number"
                            values = str(obj_profile2.phone_number)

                    if obj_profile1[0].mobil_number != obj_profile2.mobil_number:
                        old_values = old_values + "," + obj_profile1[0].mobil_number
                        if fields != "":
                            fields = fields + ",mobil number"
                            values = values + "," + obj_profile2.mobil_number
                        else:
                            fields = "mobil number"
                            values = obj_profile2.mobil_number


                    if obj_profile1[0].fk_id_type != obj_profile2.fk_id_type:
                        old_values = old_values + "," + str(obj_profile1[0].fk_id_type)
                        if fields != "":
                            fields = fields + ",document type"
                            values = values + "," + str(obj_profile2.fk_id_type)
                        else:
                            fields = "document type"
                            values = str(obj_profile2.fk_id_type)

                    if fields != "":
                        fields = fields + ",version"
                        values = values + "," +str(obj_profile2.version)
                    else:
                        fields = "version"
                        values = str(obj_profile2.version)

                    old_values = old_values + "," + str(obj_profile2.version)

                    obj_auditor_profile.field = fields
                    obj_auditor_profile.before_value = old_values
                    obj_auditor_profile.after_value = values
                    obj_auditor_profile.date = datetime.today()
                    obj_auditor_profile.user = request.user

                    state = "finish auditory edit"
                    logger.info("state: " + state + ", usuario:" + str(request.user))

                    edited = True

        except Exception as e:
            created = False
            edited = False
            logger.error("state: " + state + ", usuario:" + str(request.user) + ", error:" +e.message)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state

        if created:

            obj_profile.save()
            obj_auditor_profile.save()
            state = "create finish block"
            logger.info("state: " + state + ", usuario:" + str(request.user))

        if edited:

            obj_profile1[0].delete()
            obj_profile2.save()
            obj_auditor_profile.save()
            message = "Su perfil se ha actualizado en la base de datos"
            state = "edit finish block"
            logger.info("state: " + state + ", usuario:" + str(request.user))

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)