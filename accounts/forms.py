from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from datetime import datetime, date, timedelta

"""
    Returns a predefined html form for submitting user's preferences
"""
class AgentForm(forms.ModelForm):  
    class Meta:  
        model = AgentSearch
        fields = "__all__"
        exclude = ["agent"]

"""
    Returns a predefined html form for submitting a new user
"""
class CreateUserForm(UserCreationForm):  
    class Meta:  
        model = User  
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

"""
    Returns a predefined html form for submitting a new profile picture
"""
class UpdateProfilePic(forms.ModelForm):  
    class Meta:  
        model = Agent
        fields = ["profile_pic"]

"""
    Returns a predefined html form for submitting a date range in contact history
"""
class FilterContactDate(forms.ModelForm):
    #start_date_time = forms.DateTimeField(initial=date.today())
    #end_date_time = forms.DateTimeField(initial=date.today() + timedelta(days=1))
    start_date_time = forms.DateTimeField(initial=datetime(2021, 1, 1), widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    end_date_time = forms.DateTimeField(initial=datetime(2021, 1, 2), widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    class Meta:  
        model = ClientContact
        fields = [
            "start_date_time",
            "end_date_time"
        ]

"""
    Returns a predefined html form for submitting a contact id for agent activity
"""
class SearchContactId(forms.ModelForm):
    search_contact_id = forms.IntegerField(initial=None)
    class Meta:  
        model = ReqService
        fields = [
            "search_contact_id"
        ]
