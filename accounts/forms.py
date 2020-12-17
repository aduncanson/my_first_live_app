from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

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