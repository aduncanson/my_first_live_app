# existing django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
from .classes.tables import *
from .classes.graphs import *
from .classes.calculations import *

# external imports
from datetime import datetime, date, timedelta


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

    date_form = FilterContactDate()

    start_date_time = datetime(2021, 1, 1)
    end_date_time = datetime(2021, 1, 2)

    if request.method == "POST":
        date_form = FilterContactDate(request.POST)
        if date_form.is_valid():
            start_date_time = date_form.cleaned_data['start_date_time']
            end_date_time = date_form.cleaned_data['end_date_time']

    all_reports = contact_reports(request, None, start_date_time, end_date_time)

    call_outcome_graph = call_outcome_data(all_reports["call_outcome_table"])
    services_graph = services_data(all_reports["services_table"])
    brands_graph = brands_data(all_reports["full_contact_table"])

    stats = dailyStats(request, all_reports["full_contact_table"])

    title = "User Page"

    context = {
        "title": title,
        "date_form": date_form,
        "full_call_count": stats["full_call_count"],
        "criteria_call_count": stats["criteria_call_count"],
        "call_average": stats["call_average"],
        "oversessing": False,
        "criteria_contact_table": all_reports["criteria_contact_table"],
        "call_outcome_table": all_reports["call_outcome_table"],
        "services_table": all_reports["services_table"],
        "brands_table": all_reports["brands_table"],
        'call_outcome_graph': call_outcome_graph,
        'services_graph': services_graph,
        'brands_graph': brands_graph,
    }

    return render(request, 'accounts/agent.html', context)


# Agent specific dashboard
@login_required(login_url="login")
def agentPage(request, pk):

    exists = 0
    
    groups = request.user.groups.all()
    
    for group in groups:
        if group.name in ['Admin', 'Supervisor']:
            exists = 1

    if exists == 0:
        pk = request.user.id

    agent = Agent.objects.get(id=pk)

    date_form = FilterContactDate()

    start_date_time = datetime(2021, 1, 1)
    end_date_time = datetime(2021, 1, 2)

    if request.method == "POST":
        date_form = FilterContactDate(request.POST)
        if date_form.is_valid():
            start_date_time = date_form.cleaned_data['start_date_time']
            end_date_time = date_form.cleaned_data['end_date_time']

    all_reports = contact_reports(request, agent, start_date_time, end_date_time)

    call_outcome_graph = call_outcome_data(all_reports["call_outcome_table"])
    services_graph = services_data(all_reports["services_table"])
    brands_graph = brands_data(all_reports["full_contact_table"])

    stats = dailyStats(request, all_reports["full_contact_table"])

    title = "User Page"

    context = {
        "title": title,
        "date_form": date_form,
        "full_call_count": stats["full_call_count"],
        "criteria_call_count": stats["criteria_call_count"],
        "call_average": stats["call_average"],
        "oversessing": True,
        "agent": agent,
        "criteria_contact_table": all_reports["criteria_contact_table"],
        "call_outcome_table": all_reports["call_outcome_table"],
        "services_table": all_reports["services_table"],
        "brands_table": all_reports["brands_table"],
        'call_outcome_graph': call_outcome_graph,
        'services_graph': services_graph,
        'brands_graph': brands_graph,
    }

    return render(request, 'accounts/agent.html', context)



# Agent activity table view
@login_required(login_url="login")
@allowed_users(allowed_roles=["Admin", "Supervisor"])
def agentActivity(request, pk):

    title = "Agent Activity"

    contact_details = ReqService.objects.filter(contact_id=pk).values(
        "contact_id__agent__username",
        "contact_id__agent__first_name",
        "contact_id__agent__last_name",
        "contact_id__call_outcome",
        "contact_id__wrap_up_notes",
    ).annotate(
        comments=ArrayAgg('comments', ordering=("req_service_id")),
        services=ArrayAgg('service_type_id__service_type_name', ordering=("req_service_id")),
    )

    username = contact_details[0]["contact_id__agent__username"]
    agent_name = contact_details[0]["contact_id__agent__first_name"] + " " + contact_details[0]["contact_id__agent__last_name"]
    call_outcome = contact_details[0]["contact_id__call_outcome"]
    wrap_up_notes = contact_details[0]["contact_id__wrap_up_notes"]
    services = contact_details[0]["contact_id__wrap_up_notes"]
    comments = contact_details[0]["contact_id__wrap_up_notes"]

    context = {
        "title": title,
        "username": username,
        "agent_name": agent_name,
        "services": services,
        "comments": comments,
        "call_outcome": call_outcome,
        "wrap_up_notes": wrap_up_notes,
    }

    return render(request, 'accounts/agent_activity.html', context)
