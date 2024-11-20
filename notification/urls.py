from django import views
from  django.urls import path, include
from . import views



urlpatterns = [
    path('sms/', views.sms_deploy), # type: ignore
    path('files/',views.get_all_files, name='get_all_files')
]