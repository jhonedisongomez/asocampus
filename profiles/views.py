# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "profile_user/profile.html"
    login_url = "/inicia-sesion"
    form_class = ""

    def get(self, request, args, **kwargs):

        if "load" in request.GET: