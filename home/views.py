from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = 'home/index.html'


class SignIn(TemplateView):
    template_name = 'users/sign-in.html'




