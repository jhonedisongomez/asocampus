from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.db import connection
import logging
import uuid
from django.http import HttpResponse
import json


logger = logging.getLogger("logging")
class CountryView(LoginRequiredMixin, TemplateView):

    template_name = "country/country.html"
    form_class = ""
    login_url = "/"

    def get(self, request, *args, **kwargs ):

        is_admin = []
    
        with connection.cursor() as cursor:

            cursor.callproc('get_menu_options',[request.user.id])
            is_admin = cursor.fetchall()
    
        dic = {'menu':is_admin }
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False

        try:

            user = request.user
            state = "init"
            logger.info("state: " + state + ", usuario:" + str(request.user))

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            logger.info("data: " + str(body) + ", usuario:" + str(request.user))
            country_name = body['country_name']
            country_code = str(uuid.uuid4())
            
            with connection.cursor() as cursor:
                state = 'execute procedure create_country'
                logger.info("state: " + state + ", usuario:" + str(request.user) + ",parameters:" + country_code + "," + country_name + "," + str(user))
                
                cursor.callproc('create_country',[country_code,country_name,request.user.id])
                response_proc = cursor.fetchone()
                
                state = 'finish execute procedure create_country'
                logger.info("state: " + state + "response: "+ str(response_proc) +", usuario:" + str(request.user))
            
            is_error = response_proc[0]
            message = response_proc[1]

        except Exception as e:

            logger.error(e)
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