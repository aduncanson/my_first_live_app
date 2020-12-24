from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.safestring import mark_safe
from django.utils.html import escape

from .models import *

class AgentList(BaseDatatableView):
    """
    Agent_view = tables.LinkColumn('agent_page', text="View", args=[A("id")])

    class Meta:
        model = Agent
        fields = ["user", "user.first_name", "user.last_name", "user.email", "team_id", "team_id.department_id", "Agent_view"]
        attrs = {"class": "table table-sm"}
        orderable = False
    """
    model = Agent

"""
class AgentContactsTable(BaseDatatableView):

    contact_id__contact_date = tables.DateTimeColumn(format = 'N j, Y', footer="")
    contact_id__contact_session_id__call_start_time = tables.TimeColumn(format = 'g:i:s a')
    contact_id__contact_session_id__wrap_up_duration = tables.TimeColumn(format = 'G:i:s')
    contact_id__contact_session_id__call_end_time = tables.TimeColumn(format = 'g:i:s a')

    def render_comments(self, value):
        return mark_safe("<br>".join(value))

    def render_services(self, value):
        return mark_safe("<br>".join(value))

    class Meta:
        model = ReqService
        fields = [
            "contact_id",
            "call_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
            "comments",
            "services",
            ]
        sequence = [
            "contact_id",
            "contact_id__contact_date",
            "call_time",
            "contact_id__contact_session_id__call_start_time",
            "contact_id__contact_session_id__wrap_up_duration",
            "contact_id__contact_session_id__call_end_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
            "comments",
            "services",
        ]
        attrs = {
            "class": "table table-sm",
            "id": "agent-contacts-table"
        }
        orderable = False
"""