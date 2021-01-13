from django.contrib.auth.models import Permission, User
from django.urls import reverse
from django.db.models import *
from django.contrib.postgres.aggregates import *
from django.utils import dateparse
from django.utils.safestring import mark_safe

from ajax_datatable.views import AjaxDatatableView
from datetime import date, datetime, time, timedelta

from .models import *

"""
    Returns a table automatically formatted with Datatables js plugin, lists all agents
"""
class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent List'
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
        {'name': 'Agent Dashboard', 'visible': True, 'searchable': False, },
    ]

    # Allows customization of each row
    def customize_row(self, row, obj):
        # For 'Agent Dashboard', return it as a button
        row['Agent Dashboard'] = '<a class="btn btn-primary btn-sm btn-block" href="%s">View</a>' % (
            reverse('agent_page', args=(obj.id,))
        )

    # The initial queryset to be displayed, ignore admin users
    def get_initial_queryset(self, request=None):

        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.filter(user__is_superuser=False)

        return queryset
