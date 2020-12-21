import django_tables2 as tables
from .models import *

class AgentContacts(tables.Table):
    class Meta:
        model = ReqService
        fields = ["contact_id"]

class AgentList(tables.Table):

    my_extra_column = tables.Column(accessor='my_function',
         verbose_name='My calculated value')

    btnCol = tables.URLColumn("View")

    class Meta:
        model = Agent
        fields = ["user", "user.first_name", "user.last_name", "user.email", "team_id", "team_id.department_id", {"btnCol": "{% url 'agent_page' id %}"}]
        attrs = {"class": "table table-sm"}
