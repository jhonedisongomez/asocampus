# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import logout
import logging
from django.http import HttpResponseRedirect
logger = logging.getLogger("logging")


class SignUpView(TemplateView):
    template_name = "users/sign-up.html"
    form_class = ""

    def get(self, request, *args, **kwargs):
        if "email" in request.GET:
            try:
                state = "init"
                response_data = {}
                message = ""
                exist = False
                is_error = False
                email = request.GET['email']
                user = User.objects.filter(email=email)
                logger.info("state: " + state + ", usuario:" + str(request.user))

                state = "user"
                if user:
                    message = "ya existe una cuenta con este email"
                    exist = True

                    logger.info("state: " + state + ", usuario:" + str(request.user))
                else:
                    message = "no hay una cuenta con este email, por favor registrelo"
                    exist = False
                logger.info("state: " + state + ", usuario:" + str(request.user))
            except Exception as e:

                logger.error(e)
                is_error = True
                message = "error en el sistema por favor comuniquese con soporte"
                response_data['type_error'] = type(e).__name__

            response_data['exist'] = exist
            response_data['message'] = message
            response_data['is_error'] = is_error
            response_json = json.dumps(response_data)
            content_type = 'application/json'
            logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
            return HttpResponse(response_json, content_type)
        else:
            dic = {}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic, context_instance)

    def post(self, request, *args, **kwargs):

        try:

            state = "init"
            response_data = {}
            message = ""
            is_error = False
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            logger.info("state: " + state + ", usuario:" + str(request.user))

            first_name = body['name']
            last_name = body['last_name']
            email = body['email']
            username = email
            password = body['password']
            state = "create user"
            logger.info("state: " + state + ", usuario:" + str(request.user))
            User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            username=username,
                                            password=password)

            message = "el usuario ha sido creado por favor inicie sesion"
        except Exception as e:

            logger.error(e)
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__

        response_data['message'] = message
        response_data['is_error'] = is_error
        response_json = json.dumps(response_data)
        logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)


class SignInView(TemplateView):
    template_name = "users/sign-in.html"
    form_class = ""

    def get(self, request, *args, **kwargs):
        logger.info(str(request) +  ", usuario:" +  str(request.user))
        message = ""
        is_error = False
        authenticated = False
        response_data = {}

        if "username" in request.GET:
            try:

                username = request.GET['username']
                password = request.GET['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:

                        message = "bienvenido a nuestra plataforma"
                        authenticated = True
                        login(request, user)
                        
                        logger.info("usuario autenticado" +  ", usuario:" +  str(request.user))
                    else:
                        message = "este usuario esta desactivado por favor comuniquese con soporte"
                        logger.info("usuario desactivado" +  ", usuario:" +  str(request.user))
                else:
                    message = "Error en el nombre de usuario o contraseña"
                    logger.info("usuario no autenticado" +  ", usuario:" +  str(request.user))
            except Exception as e:
                print(e.message)
                logger.info(e +  ", usuario:" +  str(request.user))
                is_error = True
                message = "error en el sistema por favor comuniquese con soporte"
                response_data['type_error'] = type(e).__name__

            response_data['authenticated'] = authenticated
            response_data['message'] = message
            response_data['is_error'] = is_error
            response_json = json.dumps(response_data)
            logger.info("response_data: " + response_json + ", usuario:" + str(request.user))
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)

        else:
            dict = {}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dict, context_instance)


class Logout(TemplateView):

    template_name = ""
    form_class = ""

    def get(self, request, *args, **kwargs):

        try:

            message = ""
            is_error = False
            response_data = {}

            logout(request)

        except Exception as e:
            print(str(e))
            is_error = True
            message = "error en el sistema por favor comuniquese con soporte"
            response_data['type_error'] = type(e).__name__

            response_data['message'] = message
            response_data['is_error'] = is_error
            response_json = json.dumps(response_data)
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)

        return HttpResponseRedirect("/")