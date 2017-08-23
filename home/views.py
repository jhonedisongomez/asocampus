from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.db import connection

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
        is_admin = {}
        if request.user.is_authenticated():

            with connection.cursor() as cursor:

                cursor.callproc('is_administrator',[request.user.id])
                is_admin = cursor.fetchone()
        else:
		is_admin[0] = ''
		is_admin[1] = False

        dict = {'is_administrator':is_admin[1] }
        context_instance = RequestContext(request)
        template = self.template_name
        return render_to_response(template, dict, context_instance)


class SignIn(TemplateView):
    template_name = 'users/sign-in.html'





