# existing django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import *

# my django imports
from .models import *
from .forms import *
from .filters import *
from .decorators import *

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

            return redirect("home")
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

    if request.method == "POST":
        form = AgentForm(request.POST, instance=agent_search)
        if form.is_valid():
            form.save()
    
    title = "My Settings"
    
    context = {
        "title": title,
        "agent": agent,
        "form": form
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
    agents = Agent.objects.filter(user__is_superuser=False)

    myFilter = AgentListFilter(request.GET, queryset=agents)

    agents = myFilter.qs

    title = "Agent List"

    context = {
        "title": title,
        'agents': agents,
        'myFilter': myFilter
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
    agent_search = AgentSearch.objects.get(agent=request.user.agent)
    
    calls_today = ClientContact.objects.filter(
        contact_date__gte=datetime(2021,1,1),
        contact_date__lte=datetime(2021,1,7),
        agent_id=agent.user,
        contact_session_id__brand_id__in=agent_search.brands.all()
    ).order_by("contact_date")

    myFilter = AgentFilter(request.GET, queryset=calls_today)

    calls_today = myFilter.qs
    
    calls_today_count = calls_today.count()

    statistics = calls_today.aggregate(
        avg=Avg(F('contact_session_id_id__call_end_time') - F('contact_session_id_id__call_start_time')),
        max=Max(F('contact_session_id_id__call_end_time') - F('contact_session_id_id__call_start_time')),
    )

    calls_today_range = calls_today.annotate(
        call_time=F('contact_session_id_id__call_end_time') - F('contact_session_id_id__call_start_time')
    )

    calls_today_range = calls_today_range.filter(
        call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit]
    ).order_by("contact_date")

    title = "User Page"

    context = {
        "title": title,
        "calls_today": calls_today,
        "calls_today_count": calls_today_count,
        "avg": statistics["avg"],
        "max": str(round(calls_today_range.count()/calls_today_count*100, 2)) + "%",
        "myFilter": myFilter,
        "agent_search": agent_search,
        "ranged_count": calls_today_range,
    }

    return render(request, 'accounts/agent.html', context)
