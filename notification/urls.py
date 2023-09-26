from  django.urls import path, include
from .views import send_email, send_sms




urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path("", send_email, name='mail'),
    path("sms/",send_sms, name='sms')
]
