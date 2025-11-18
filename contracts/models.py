# from contextlib import nullcontext
from django.db import models
from django.contrib.auth.models import User
import os
from auditlog.registry import auditlog




class FiscalYear(models.Model):
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_year}/{self.end_year}"

auditlog.register(FiscalYear)


class Roles(models.Model):
    name = models.CharField(max_length=20)

auditlog.register(Roles)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    bio = models.TextField()
    otp = models.BooleanField(default=False)
    roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username   
auditlog.register(Profile)


def office_docuemnt_path(instance, filename):
    return os.path.join('office_name', instance.office_name, filename)

class Office_name (models.Model):
    office_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pan_no = models.IntegerField(null=True)
    document = models.FileField(upload_to=office_docuemnt_path, null=True, blank=True)
    extra = models.JSONField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str_(self):
        return self.office_name

auditlog.register(Office_name)

class Client(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=15, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str_(self):
        return self.name

auditlog.register(Client)

class Contracts(models.Model):
    office = models.ForeignKey(Office_name, on_delete=models.CASCADE)
    title_of_contract = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fiscalyear = models.ForeignKey(FiscalYear, on_delete=models.DO_NOTHING, null=True)
    contract_date = models.DateField(null=True, blank=True)
    billing_date = models.DateField(null=True, blank=True)
    amount = models.FloatField(null=True)
    payment_status = models.BooleanField(default=False, null=True)
    status = models.IntegerField(default=1)
    comission = models.FloatField(blank=True, null=True)
    contract_file = models.FileField(upload_to='media')
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


auditlog.register(Contracts)

class Contract_actions(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    amount = models.IntegerField(blank=True)
    extra = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(max_length=20000, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


auditlog.register(Contract_actions)
class OtpToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    otp = models.IntegerField(default=0)
    purpose  = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    extra = models.JSONField(null=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

auditlog.register(OtpToken)