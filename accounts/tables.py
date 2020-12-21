import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class AgentContacts(tables.Table):
    class Meta:
        model = ReqService
        fields = ["contact_id"]

class AgentList(tables.Table):

    Agent_view = tables.LinkColumn('agent_page', text="View", args=[A("pk")])

    class Meta:
        model = Agent
        fields = ["user", "user.first_name", "user.last_name", "user.email", "team_id", "team_id.department_id", "Agent_view"]
        attrs = {"class": "table table-sm"}
