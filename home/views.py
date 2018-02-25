# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

"""
TODO: crear return para menu
crear procedmiento almacenado para obtener el menu
crear tabla para menu
crear roles
crear menu para los tipos de roles.
"""
class IndexView(TemplateView):
    template_name = 'home/index.html'
    form_class = ""

    def get(self, request, *args, **kwargs):
        is_admin = []
        dict = {}
        """if request.user.is_authenticated():

            with connection.cursor() as cursor:

                cursor.callproc('get_menu',[request.user.id])
                is_admin = cursor.fetchall()
        
        dict = {'menu':is_admin }"""
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dict, context_instance)


class SignIn(TemplateView):
    template_name = 'users/sign-in.html'


class baseSuperAdminView(LoginRequiredMixin,TemplateView):
    template_name = 'home/index-superadmin.html'
    form_class = ""
    login_url = "/"

    def get(self, request, *args, **kwargs):
        is_admin = []
        if request.user.is_authenticated():

            with connection.cursor() as cursor:

                cursor.callproc('get_menu_options',[request.user.id])
                is_admin = cursor.fetchall()
        
        dict = {'menu':is_admin }
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dict, context_instance)


