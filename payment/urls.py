from django.conf.urls import url
from .views import PaymentView

urlpatterns = [
    url(r'^pago-de-actividad/$', PaymentView.as_view(),name='payment-activity'),

]
