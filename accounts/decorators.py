from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

"""
    If the user logs in successfully, redirect them to 'dashboard' view
"""
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

"""
    If the user doesn't have permission to view, redirect them to their 'agent_page' view
"""
def allowed_users(allowed_roles=[]):
    def decorator (view_func):
        def wrapper_func(request, *args, **kwargs):
            
            groups = None
            exists = None
            
            # Check the user is in some permission group
            if request.user.groups.exists():
                groups = request.user.groups.all()
            
            # Check if their group is one of the permitted ones
            for group in groups:
                if group.name in allowed_roles:
                    exists = 1

            # If they have permission, take them to view, otherwise redirect them to their 'agent_page' view
            if exists == 1:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("agent_page", request.user.id)
        return wrapper_func
    return decorator
