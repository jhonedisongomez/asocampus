from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from .forms import VerifySignUpForm
from activities.models import signUpActivities, Activities
from .models import *
import threading


#get functions
def validatePayPerson(request):

    message = ""
    is_error = False
    is_sign_up_db = False
    is_paied = False
    is_sign_up = False
    response_data = {}

    try:

        #get the information from form html
        email = request.GET['email']
        activity_pk = request.GET['activity']

        #query to validate if the user exist in the database
        obj_user = User.objects.filter(email = email, is_active = True)

        if obj_user:
            is_sign_up_db = True
            obj_user = User.objects.get(id= obj_user[0].pk)

            #search pay
            obj_activity = Activities.objects.filter(pk = activity_pk)
            activity_code = obj_activity[0].activities_code
            obj_payment = Payment.objects.filter(active = True, fk_activity_code = activity_code)
            payment_code = obj_payment[0].payment_code


            obj_signUpActivities = signUpActivities.objects.filter(active = True, fk_user = obj_user)

            if obj_signUpActivities:
                is_sign_up = True
                obj_paymentPerson = PaymentPerson.objects.filter(fk_payment_code = payment_code,fk_user_paied = obj_user)
                if obj_paymentPerson:

                    message = "el usuario ya cancelo la inscripcion, puede descargar su escarapela"
                    is_paied = True
                else:
                    message = "el usuario no ha pagado la actividad"
            else:

                message = "el usuario no esta registrado en esta actividad, por favor registrelo"

        else:

            message = "el usuario no existe en la base de datos, por favor registrelo"

    except Exception as e:

        is_error = True
        message = "error en el sistema por favor comuniquese con soporte"
        response_data['type_error'] = type(e).__name__

    response_data['message'] = message
    response_data['is_error'] = is_error
    response_data['is_paied'] = is_paied
    response_data['is_sign_up_db'] = is_sign_up_db
    response_data['is_sign_up'] = is_sign_up

    return response_data

#post functions

def savePAgePerson(request):

    response_data = {}
    message = ""
    is_error = False

    email = request.POST['email']
    activity_pk = request.POST['activity']

    obj_activity = Activities.objects.filter(pk = activity_pk)
    activity_code = obj_activity[0].activities_code

    obj_payment = Payment.objects.filter(active = True, fk_activity_code = activity_code)
    payment_code = obj_payment[0].payment_code

    #user that pay the activity
    obj_user = User.objects.get(email = email, is_active = True)

    obj_paymentPerson = PaymentPerson()
    obj_paymentPerson.fk_payment_code = payment_code
    obj_paymentPerson.fk_user_created = request.user
    obj_paymentPerson.fk_user_paied = obj_user
    obj_paymentPerson.save()

    message = "se ha registrado el pago en la base de datos, la escarapela se descargara en un momento"

    response_data['message'] = message
    response_data['is_error'] = is_error

    return response_data

class PaymentView(TemplateView, LoginRequiredMixin):

    template_name = "payment/create-payment.html"
    login_url = "/"
    form_class = VerifySignUpForm()
    lock = threading.Lock()
    def get(self, request, *args, **kwargs):

        self.lock.acquire()

        if "method" in request.GET:

            method = request.GET['method']
            method = eval(method)

            response_json = json.dumps(method)
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)
        else:


            dic = {'form': self.form_class}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, dic,context_instance)
        lock.release()
        
    def post(self, request, *args, **kwargs):

        self.lock.acquire()
        method = request.POST['method']
        method = eval(method)

        response_json = json.dumps(method)
        content_type = 'application/json'
        return HttpResponse(response_json, content_type)
        lock.release()
