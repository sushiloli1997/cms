from django.contrib import admin
from .models import Contract_actions, Contracts,Profile, Client, Roles, FiscalYear
# Register your models here.

admin.site.register(Contract_actions)
admin.site.register(Profile)
admin.site.register(Client)

admin.site.register(Contracts)
admin.site.register(Roles)
admin.site.register(FiscalYear)
