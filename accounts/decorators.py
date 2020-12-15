from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator (view_func):
        def wrapper_func(request, *args, **kwargs):
            
            groups = None
            exists = None
            
            if request.user.groups.exists():
                groups = request.user.groups.all()
            
            for group in groups:
                if group.name in allowed_roles:
                    exists = 1

            if exists == 1:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("agent_page", request.user.id)
        return wrapper_func
    return decorator
