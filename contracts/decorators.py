from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, * args, **kwargs)
    return wrapper_func






def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            role_id = None
            # if request.user.profile.roles.id.exists():
            #     role_id = request.user.profile.roles.all()[0].id
            
            role_id= request.user.profile.roles.id
            # print(role_id)
            if role_id in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Unauthorized Access')
                return redirect ('dashboard')    
        return wrapper_func
    return decorator
