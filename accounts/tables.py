import django_tables2 as tables
from .models import *

class AgentContacts(tables.Table):
    class Meta:
        model = ReqService
        fields = ["contact_id"]

class AgentList(tables.Table):

    btnCol = tables.TemplateColumn("<a class='btn btn-sm btn-info' href='{% url 'agent_page' agent.id %}'>View</a>")

    class Meta:
        model = Agent
        fields = ["user", "user.first_name", "user.last_name", "user.email", "team_id", "team_id.department_id", "btnCol"]
        attrs = {"class": "table table-sm"}
