from  django.urls import path
from .views import send_email, sms

urlpatterns = [
    path("", send_email, name='mail'),
    path("sms/",sms, name='sms')
]
