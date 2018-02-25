# -*- coding: utf-8 -*-
import json
import uuid
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db import connection

logger = logging.getLogger("logging")


class ProfileView(TemplateView, LoginRequiredMixin):

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

                    cursor.callproc('get_profile_activity', [request.user.id])
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
        state = "init"
        response = []

        try:
            method = request.POST['method']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            document = int(request.POST['document_id'])
            document_type = int(request.POST['document_type'])
            phone = request.POST['phone']
            if phone != '':
                phone = int(phone)

            else:
                phone = 0

            mobil_number = request.POST['mobil_number']
            birthday = request.POST['birthday']
            if method == "create":

                if request.user.is_authenticated():
                    profile_code = str(uuid.uuid4())
                    with connection.cursor() as cursor:

                        cursor.callproc('create_profile', [profile_code, document, first_name, last_name, phone,
                                                           mobil_number, document_type, request.user.id])
                        response = cursor.fetchone()

                dic = {'is_error': response[0],
                       'message': response[1]}
                context_instance = RequestContext(request)
                template = self.template_name
                return render_to_response(template, dic, context_instance)

            if method == "edit":

                print('edit')

        except Exception as e:

            logger.error("state: " + state + ", usuario:" + str(request.user) + ", error:" +e.message)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state


        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)