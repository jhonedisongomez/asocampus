# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, IdType, AuditorProfile
import logging

logger = logging.getLogger("logging")


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "profile/profile.html"
    class_form = ""
    login_url = "/inicia-sesion/"

    def get(self, request, *args, **kwargs):

        state = "init"
        logger.info("state: " + state + ", usuario:" + str(request.user))
        response_data = {}
        profile_data = {}
        data = []
        message = ""
        is_error = False
        created = False

        if "load" in request.GET:
            try:

                state = "validate profile"
                logger.info("state: " + state + ", usuario:" + str(request.user))
                obj_profile = Profile.objects.filter(active=True,fk_user=request.user )

                if obj_profile:

                    profile_data['document_id'] = obj_profile[0].document_id
                    profile_data['name'] = obj_profile[0].first_name + " " + obj_profile[0].last_name
                    profile_data['mobil_number'] = obj_profile[0].movil_number
                    profile_data['email'] = request.user.email
                    data.append(profile_data)
                    response_data['data'] = data

            except Exception as e:
                print (e)
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

        message = ""
        is_error = False
        created = False
        state = "init"
        logger.info("state: " + state + ", usuario:" + str(request.user))

        try:

            if "method" in request.POST:

                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)

                method = body['method']

                if method == "create":

                    state = "init create"
                    logger.info("state: " + state + ", usuario:" + str(request.user))
                    obj_id_type = IdType.objects.filter(pk=body['id_type'])

                    obj_profile = Profile()
                    obj_profile.document_id = body['id']
                    obj_profile.first_name = body['first_name']
                    obj_profile.last_name = body['last_name']
                    obj_profile.phone_number = body['phone_number']
                    obj_profile.movil_number = body['mobil_number']
                    obj_profile.fk_id_type = obj_id_type[0].pk
                    obj_profile.fk_user = request.user

                    obj_auditor_profile = AuditorProfile()
                    obj_auditor_profile.action = "CREATE"
                    obj_auditor_profile.table = "Profile"
                    obj_auditor_profile.field = "ALL"
                    obj_auditor_profile.after_value = obj_profile.profile_code + "," + obj_profile.document_id +"," \
                    + obj_profile.first_name + "," + obj_profile.last_name + "," + obj_profile.phone_number + "+" \
                    + obj_profile.movil_number + "," + obj_profile.active + "," + obj_profile.fk_id_type + "," \
                    + obj_profile.fk_user

                    obj_auditor_profile.user = request.user

                    message = "Su perfil ha sido guardado en la base de datos"
                    state = "finish create"
                    logger.info("state: " + state + ", usuario:" + str(request.user))

        except Exception as e:

            state = "error"
            logger.error("state: " + state + ", usuario:" + str(request.user) + ", error:" + e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state

        if created:

            obj_profile.save()
            obj_auditor_profile.save()
            state = "save finish block"
            logger.info("state: " + state + ", usuario:" + str(request.user))

        response_data['message'] = message
        response_data['is_error'] = is_error

        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)