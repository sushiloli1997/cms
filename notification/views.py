from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
# # import  smtplib, ssl

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



class Notification:
    def __init__(self, email, msg, number):
        self.number = number
        self.email= email
        self.msg = msg
    

    def sms(self, request):
        url=settings.SMS_URL
        token = settings.SMS_TOKEN

