from django.test import TestCase

# Create your tests here.


class Notification:
    def __init__(self, mobile, sms):
        self.mobile = mobile
        self.sms = sms




new = Notification(9844955757, 'this is test')

print(new.sms)