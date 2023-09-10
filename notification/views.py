from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
# # import  smtplib, ssl
from django.views import View
import requests, json

# # Create your views here.


# def send_email(request):
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = 'sushil.ctri@gmail.com'
#     # context = ssl.create_default_context()
#     send_mail('sushil','new thank you',email_from, [recipient_list])


import smtplib
from email.mime.text import MIMEText


def send_email(request):
    # SMTP server and port
    smtp_server = settings.EMAIL_HOST
    smtp_port = 587

    # Your email and password
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    # Recipient email
    recipient_email = 'sushil@sttnepal.com'

    # Create the message
    message = MIMEText('Hello, this is a test email.')
    message['Subject'] = 'Test Email'
    message['From'] = sender_email
    message['To'] = recipient_email

    # Connect to the SMTP server
    # print("test")
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS encryption
            server.starttls()

            # Log in to the server
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
            
    except Exception:
        return HttpResponse("<h1>Error</h1>")

    return HttpResponse(request, 'Email sent successfully.')



def sms(request):
    # message_text = request.POST['msg-token']
    mobile_number= '9844955757'
    message_text= "Thank You for your donation"
    # mobile_number = request.POST['phone-number']
    headers = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Method':'POST',
            'Authorization':"Bearer " +settings.SMS_TOKEN,
        }

    body ={
    "message": message_text,
    "mobile": mobile_number,
    }
    url = 'https://sms.sociair.com/api/sms'
    send_sms = requests.post(url, headers=headers,data=json.dumps(body))
    # Logs = Sms_logs(number= mobile_number, sms_text= message_text, created_at=datetime.datetime.now())
    # print(Logs)
        # Logs.save()
    status_send_sms = send_sms.text

    print(status_send_sms)
    return render(request, 'home/index.html')




        

    def get(self, request):
        pass

