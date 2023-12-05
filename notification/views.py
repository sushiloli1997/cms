from django.shortcuts import render, HttpResponse
from django.conf import settings

import requests, json
from django.http import JsonResponse





class Notification:
    def __init__(self, mobile, msg):
        self.mobile = mobile
        self.msg = msg


    def sms(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + settings.SMS_TOKEN,
        }
        body = {
            "message": self.msg,
            "mobile": self.mobile,
        }
        url = 'https://sms.sociair.com/api/sms'
        try:
            request= requests.post(url, headers=headers, data=json.dumps(body))
            # dd(request)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)




def send_sms():
    pass
    

def sms_deploy(request):
    Notification('this is test sms','9844955757').sms()
    return HttpResponse ("This is test")


def emailNotification(request):
    pass
