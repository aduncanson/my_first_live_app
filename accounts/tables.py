import django_tables2 as tables
from .models import *

class AgentContacts(tables.Table):
    class Meta:
        model = ReqService
        fields = ["contact_id"]

class AgentList(tables.Table):
    class Meta:
        model = Agent
        fields = ["user", "first_name", "last_name", "email", "team_id", "team_id.department_id"]
