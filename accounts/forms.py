from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
import datetime

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
    start_date_time = forms.DateTimeField(initial=datetime.date.today)
    end_date_time = forms.DateTimeField(initial=datetime.date(year=today.year, month=today.month, day=today.day+1))
    class Meta:  
        model = ClientContact
        fields = [
            "start_date_time",
            "end_date_time"
        ]