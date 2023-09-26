from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
# # import  smtplib, ssl
from django.views import View
import requests, json
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText










def send_email(request):
    pass



def sms(request, mobile, msg):
    dd(request)
    mobile_number = mobile
    message_text = msg

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + settings.SMS_TOKEN,
    }

    body = {
        "message": message_text,
        "mobile": mobile_number,
    }

    url = 'https://sms.sociair.com/api/sms'
    try:
        send_sms = requests.post(url, headers=headers, data=json.dumps(body))
        send_sms.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return JsonResponse(send_sms.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)



        
def send_sms(msg, mobile):
    test = sms(None, mobile, msg)

    return HttpResponse(test)

# send_sms('this istests sms','9844955757')