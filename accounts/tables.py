import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class AgentList(tables.Table):

    Agent_view = tables.LinkColumn('agent_page', text="View", args=[A("id")])

    class Meta:
        model = Agent
        fields = ["user", "user.first_name", "user.last_name", "user.email", "team_id", "team_id.department_id", "Agent_view"]
        attrs = {"class": "table table-sm"}
        orderable = False


class AgentContactsTable(tables.Table):

    contact_id__contact_date = tables.DateTimeColumn(format = 'N j, Y')

    class Meta:
        model = ReqService
        fields = [
            "contact_id",
            "call_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
            "contact_id__contact_date",
            ]
        sequence = [
            "contact_id",
            "call_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
            "contact_id__contact_date",
        ]
        attrs = {"class": "table table-sm"}
        orderable = False
