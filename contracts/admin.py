from django.contrib import admin
from .models import Contract_actions,Profile, Client
# Register your models here.

admin.site.register(Contract_actions)
admin.site.register(Profile)
admin.site.register(Client)