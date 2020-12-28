from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission, User

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent'
    initial_order = [["user_id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'Username', 'foreign_field': 'user__username', 'visible': True, },
        {'name': 'First Name', 'foreign_field': 'user__first_name', 'visible': True, },
        {'name': 'Surname', 'foreign_field': 'user__last_name', 'visible': True, },
        {'name': 'Email', 'foreign_field': 'user__email', 'visible': True, },
        {'name': 'Team', 'foreign_field': 'team__team_name', 'visible': True, },
        {'name': 'Department', 'foreign_field': 'team__department__department_name', 'visible': True, },
    ]


 "user.email", "team_id", "team_id.department_id", "Agent_view"]