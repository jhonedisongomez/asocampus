# -*- coding: utf-8 -*-
import logging
import uuid
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connection
from django.http import HttpResponse

logger = logging.getLogger("logging")


class CountryView(LoginRequiredMixin, TemplateView):

    template_name = "country/country.html"
    form_class = ""
    login_url = "/"
    menu = []
    list_country = []
    response_data = {}
    is_error = False
    is_admin = False
    message = ''
    response_proc = []

    def get(self, request, *args, **kwargs ):

        try:
            if "load" in request.GET:

                state = "init"
                logger.info("state: " + state + "CountryView, get" + ", usuario:" + str(request.user))
                with connection.cursor() as cursor:

                    state = 'finish execute procedure create_country'
                    logger.info("state: " + state + "call procedure: getCountry, usuario:" + str(request.user))

                    cursor.callproc('getCountry',[request.user.id, request.GET['country_code']])
                    self. response_proc = cursor.fetchone()

                state = 'finish execute procedure getCountry'
                logger.info("state: " + state + "response: "+ str(self. response_proc) +", usuario:" + str(request.user))

                self.response_data['country_name'] = self.response_proc[0]
                self.response_data['is_active'] = self.response_proc[1]
                self.response_data['message'] = self. response_proc[2]
                self.response_data['is_error'] = self. response_proc[3]
                self.response_data['is_Admin'] = self. response_proc[4]
                response_json = json.dumps(self.response_data)
                logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
                content_type = 'application/json'
                return HttpResponse(response_json, content_type)

            else:

                # get urls to menu
                with connection.cursor() as cursor:

                    state = "get menu options"
                    cursor.callproc('get_menu_options',[request.user.id])
                    self.menu = cursor.fetchall()

                    state = "get list country"

                    #get list of countries for table
                    cursor.callproc('list_country',[request.user.id])
                    self.list_country = cursor.fetchall()

                dic = {'menu':self.menu,
                       'countries': self.list_country}

                context_instance = RequestContext(request)
                template = self.template_name
                return render_to_response(template, dic,context_instance)

        except Exception as e:

            logger.error(e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            self.response_data['type_error'] = type(e).__name__
            self.response_data['file'] = "activities view"
            self.response_data['class'] = "ActivitiesView"
            self.response_data['state'] = state

            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)

    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        response_proc = []

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

                if(body['method'] == 'create'):

                    state = 'execute procedure create_country'
                    logger.info("state: " + state + ", usuario:" + str(request.user) + ",parameters:" + country_code + "," + country_name + "," + str(user))

                    cursor.callproc('create_country',[country_code,country_name,request.user.id])
                    response_proc = cursor.fetchone()

                    state = 'finish execute procedure create_country'
                    logger.info("state: " + state + "response: "+ str(response_proc) +", usuario:" + str(request.user))

                if(body['method'] == 'edit'):

                    country_code = body['country_code']
                    active = body['is_active']
                    state = 'execute procedure edit_country'
                    logger.info("state: " + state + ", usuario:" + str(request.user) + ",parameters:" + country_code + "," + country_name + "," + str(user))

                    cursor.callproc('edit_country',[country_code
                        ,country_name,active,request.user.id])
                    response_proc = cursor.fetchone()

                    state = 'finish execute procedure edit'
                    logger.info("state: " + state + "response: "+ str(response_proc) +", usuario:" + str(request.user))

            #message, is error, is admin
            message = response_proc[0]
            is_error = response_proc[1]

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


class SectionTypeView(LoginRequiredMixin,TemplateView):

    template_name = "country/section-type.html"
    form_class = ""
    login_url = "/"
    menu = []
    list_section_type = []
    response_data = {}
    is_error = False
    is_admin = False
    message = ''
    response_proc = []

    def get(self, request, *args, **kwargs):

        try:

            if "load" in request.GET:

                state = "init"
                logger.info("state: " + state + "SectionTypeView, get" + ", usuario:" + str(request.user))
                with connection.cursor() as cursor:

                    state = 'init call procedure get sectionType'
                    logger.info("state: " + state + " , usuario:" + str(request.user))

                    cursor.callproc('get_section_type',[request.user.id, request.GET['section_type_code']])
                    self. response_proc = cursor.fetchone()

                state = 'finish execute procedure getSectionType'
                logger.info("state: " + state + "response: "+ str(self. response_proc) +", usuario:" + str(request.user))

                self.response_data['section_type_name'] = self.response_proc[0]
                self.response_data['is_active'] = self.response_proc[1]
                self.response_data['message'] = self. response_proc[2]
                self.response_data['is_error'] = self. response_proc[3]
                self.response_data['is_Admin'] = self. response_proc[4]
                response_json = json.dumps(self.response_data)
                logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
                content_type = 'application/json'
                return HttpResponse(response_json, content_type)

            else:

                # get urls to menu
                with connection.cursor() as cursor:

                    state = "get menu options"
                    cursor.callproc('get_menu_options',[request.user.id])
                    self.menu = cursor.fetchall()

                    state = "get list section types"

                    #get list of countries for table
                    cursor.callproc('list_section_types',[request.user.id])
                    self.list_section_type = cursor.fetchall()

                dic = {'menu':self.menu,
                       'section_types': self.list_section_type}

                context_instance = RequestContext(request)
                template = self.template_name
                return render_to_response(template, dic,context_instance)


        except Exception as e:

            logger.error(e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            self.response_data['type_error'] = type(e).__name__
            self.response_data['file'] = "section type view"
            self.response_data['class'] = "SectionTypeView"
            self.response_data['state'] = state

            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)


    def post(self, request, *args, **kwargs):

        response_data = {}
        message = ""
        is_error = False
        response_proc = []

        try:

            user = request.user
            state = "init section type view post"
            logger.info("state: " + state + ", usuario:" + str(request.user))

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            logger.info("data: " + str(body) + ", usuario:" + str(request.user))
            section_type_name = body['section_type_name']
            section_type_code = str(uuid.uuid4())

            with connection.cursor() as cursor:

                if(body['method'] == 'create'):

                    state = 'execute procedure create_section_type'
                    logger.info("state: " + state + ", usuario:" + str(request.user) + ",parameters:" + section_type_code + "," + section_type_name + "," + str(user))

                    cursor.callproc('create_section_type',[section_type_code,section_type_name,request.user.id])
                    response_proc = cursor.fetchone()

                    state = 'finish execute procedure create_section_type'
                    logger.info("state: " + state + "response: "+ str(response_proc) +", usuario:" + str(request.user))

                if(body['method'] == 'edit'):

                    section_type_code = body['section_type_code']
                    active = body['is_active']
                    state = 'execute procedure edit_section_type'
                    logger.info("state: " + state + ", usuario:" + str(request.user) + ",parameters:" + section_type_code + "," + section_type_name + "," + str(user))

                    cursor.callproc('edit_section_type',[section_type_code
                        ,section_type_name,active,request.user.id])
                    response_proc = cursor.fetchone()

                    state = 'finish execute procedure edit section type'
                    logger.info("state: " + state + "response: "+ str(response_proc) +", usuario:" + str(request.user))

            #message, is error, is admin
            self. message = response_proc[0]
            self.is_error = response_proc[1]

        except Exception as e:

            logger.error(e)
            self.is_error = True
            self.message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__
            response_data['state'] = state

        response_data['message'] = self.message
        response_data['is_error'] = self.is_error
        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
