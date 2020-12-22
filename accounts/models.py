from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.brand_name

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.department_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=200, null=True)
    department_id = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.team_name

class ServiceType(models.Model):
    service_type_id = models.AutoField(primary_key=True)
    service_type_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.service_type_name

class Agent(models.Model):
    user = models.OneToOneField(User, unique=True, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    team_id = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class AgentSearch(models.Model):
    agent = models.OneToOneField(Agent, unique=True, null=True, blank=True, on_delete=models.CASCADE)
    brands = models.ManyToManyField(Brand)
    teams = models.ManyToManyField(Team)
    call_lower_limit = models.TimeField(default=datetime.now().time().replace(hour=0, minute=0, second=0, microsecond=0), null=True)  
    call_upper_limit = models.TimeField(default=datetime.now().time().replace(hour=0, minute=5, second=0, microsecond=0), null=True)

    def __str__(self):
        return self.agent.user.username

class ContactSession(models.Model):
    contact_session_id = models.AutoField(primary_key=True)
    call_start_time = models.TimeField(blank=True, null=True)
    wrap_up_duration = models.TimeField(blank=True, null=True)
    call_end_time = models.TimeField(blank=True, null=True)
    call_type = models.IntegerField(blank=True, null=True)
    dialled = models.IntegerField(blank=True, null=True)
    brand_id = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.contact_session_id)
        

class ClientContact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_session_id = models.ForeignKey(ContactSession, null=True, blank=True, on_delete=models.SET_NULL)
    agent = models.ForeignKey(User, to_field='username', null=True, blank=True, on_delete=models.SET_NULL)
    contact_date = models.DateTimeField(blank=True, null=True)
    call_outcome = models.CharField(max_length=200, blank=True, null=True)
    wrap_up_notes = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.contact_id)

    @property
    def reqServce(self, contact_id):
        return "ytre"

class ReqService(models.Model):
    req_service_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(ClientContact, null=True, blank=True, on_delete=models.SET_NULL)
    service_type_id = models.ForeignKey(ServiceType, null=True, blank=True, on_delete=models.SET_NULL)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.req_service_id)
