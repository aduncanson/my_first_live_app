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


class AgentContacts(tables.Table):

    class Meta:
        model = ReqService
        fields = [
            "contact_id",
            "contact_id.contact_dat",
            "contact_id.call_time",
            "contact_id.contact_session_id.call_start_time",
            "contact_id.contact_session_id.wrap_up_duration",
            "contact_id.contact_session_id.call_end_time",
            "contact_id.call_outcome",
            "contact_id.wrap_up_notes",
            "contact_id.contact_session_id.call_type",
            "contact_id.contact_session_id.dialled",
            "contact_id.contact_session_id.brand_id",
            ]
        attrs = {"class": "table table-sm"}
        orderable = False
