from django.contrib.auth.models import Permission, User
from django.urls import reverse

from ajax_datatable.views import AjaxDatatableView

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent'
    initial_order = [["Username", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'Username', 'foreign_field': 'user__username', 'visible': True, },
        {'name': 'First Name', 'foreign_field': 'user__first_name', 'visible': True, },
        {'name': 'Surname', 'foreign_field': 'user__last_name', 'visible': True, },
        {'name': 'Email', 'foreign_field': 'user__email', 'visible': True, },
        {'name': 'Team', 'foreign_field': 'team_id__team_name', 'visible': True, },
        {'name': 'Department', 'foreign_field': 'team_id__department_id__department_name', 'visible': True, },
        {'name': 'Agent Dashboard', 'visible': True, 'className': 'btn btn-primary btn-sm btn-block', },
    ]

    def customize_row(self, row, obj):
        row['Agent Dashboard'] = '<a href="%s">View</a>' % (
            reverse('agent_page', args=(obj.id,))
        )
