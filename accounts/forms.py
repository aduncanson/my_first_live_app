from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from datetime import datetime, date, timedelta

class AgentForm(forms.ModelForm):  
    class Meta:  
        model = AgentSearch
        fields = "__all__"
        exclude = ["agent"]

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

class UpdateProfilePic(forms.ModelForm):  
    class Meta:  
        model = Agent
        fields = ["profile_pic"]

class MinContactDate(forms.ModelForm):  
    class Meta:  
        model = ClientContact
        fields = [
            "contact_date"
        ]

class FilterContactDate(forms.ModelForm):
    #start_date_time = forms.DateTimeField(initial=date.today())
    #end_date_time = forms.DateTimeField(initial=date.today() + timedelta(days=1))
    start_date_time = forms.DateTimeField(initial=datetime(2021, 1, 1))
    end_date_time = forms.DateTimeField(initial=datetime(2021, 1, 2))
    class Meta:  
        model = ClientContact
        fields = [
            "start_date_time",
            "end_date_time"
        ]

class SearchContactId(forms.ModelForm):
    class Meta:  
        model = ReqService
        fields = [
            "contact_id"
        ]
