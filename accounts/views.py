# existing django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import *
from django.contrib.postgres.aggregates import *
from django.utils.safestring import mark_safe

# my django imports
from .models import *
from .forms import *
from .decorators import *
from .classes.reports import *

# external imports
from datetime import datetime


"""
----------------------------------------------------------------------------------------
--------------------------------- ACCESSING SITE VIEWS ---------------------------------
----------------------------------------------------------------------------------------
"""


# Displays the page to register user
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.is_active = False
            user = form.save()
            
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for '" + username + "'.")

            return redirect('login')

    title = "Register"

    context = {
        "title": title,
        'form': form
    }

    return render(request, 'accounts/register.html', context)


# Displays the login page
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("dashboard")
        else:
            messages.info(request, "Username or password is incorrect.")
    
    title = "Login"
    
    context = {
        "title": title
    }

    return render(request, 'accounts/login.html', context)


# Logs out the user and redirects to the Login page
def logoutUser(request):
    logout(request)

    return redirect("login")


"""
----------------------------------------------------------------------------------------
---------------------------------- USER SETTING VIEWS ----------------------------------
----------------------------------------------------------------------------------------
"""


# Displays the user's setting
@login_required(login_url="login")
@allowed_users(allowed_roles=["Admin", "Supervisor", "Agent"])
def agentSettings(request):
    agent = request.user.agent
    agent_search = AgentSearch.objects.get(agent=agent)
    form = AgentForm(instance=agent_search)
    profilePic = UpdateProfilePic(instance=agent)

    if request.method == "POST":
        form = AgentForm(request.POST, instance=agent_search)
        if form.is_valid():
            form.save()
    
    title = "My Settings"
    
    context = {
        "title": title,
        "agent": agent,
        "form": form,
        "profilePic": profilePic,
    }

    return render(request, 'accounts/agent_settings.html', context)


"""
----------------------------------------------------------------------------------------
----------------------------------- NON-AGENT VIEWS -----------------------------------
----------------------------------------------------------------------------------------
"""


# Displays a list of all agents and links to their dashboards
@login_required(login_url="login")
@allowed_users(allowed_roles=["Admin", "Supervisor"])
def agentList(request):

    title = "Agent List"

    context = {
        "title": title,
    }

    return render(request, 'accounts/agent_list.html', context)


"""
----------------------------------------------------------------------------------------
----------------------------------- ALL AGENT VIEWS -----------------------------------
----------------------------------------------------------------------------------------
"""


# The dashboard admin and supervisors are taken to upon login
@login_required(login_url="login")
@allowed_users(allowed_roles=["Admin", "Supervisor"])
def dashboard(request):
    calls_today = ClientContact.objects.all()
    calls_today_count = calls_today.filter().count()

    title = "Dashboard"

    context = {
        "title": title,
        'calls_today': calls_today,
        'calls_today_count': calls_today_count,
    }

    return render(request, 'accounts/dashboard.html', context)


# Agent specific dashboard
@login_required(login_url="login")
@allowed_users(allowed_roles=["Admin", "Agent"])
def agentPage(request, pk):
    agent = Agent.objects.get(id=pk)
    """
    statistics = agent_contacts["all_calls_with_ct"].aggregate(
        avg=Avg(F('contact_id_id__contact_session_id_id__call_end_time') - F('contact_id_id__contact_session_id_id__call_start_time')),
        max=Max(F('contact_id_id__contact_session_id_id__call_end_time') - F('contact_id_id__contact_session_id_id__call_start_time')),
    )"""

    title = "User Page"

    table = ReqService.objects.filter(contact_id__agent=agent.user).values(
        "contact_id_id",
    ).annotate(
        comments=ArrayAgg('comments', ordering=("req_service_id")),
        services=ArrayAgg('service_type_id__service_type_name', ordering=("req_service_id")),
        call_time=F('contact_id__contact_session_id__call_end_time') - F('contact_id__contact_session_id__call_start_time'),
    )

    context = {
        "title": title,
        "calls_today_count": 100,
        "avg": 123,
        "max": 1,
        "ranged_count": 2,
        "oversessing": True,
        "agent": agent,
        "table": table,
    }

    return render(request, 'accounts/agent.html', context)
