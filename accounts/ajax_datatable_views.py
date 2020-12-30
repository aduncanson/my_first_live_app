from django.contrib.auth.models import Permission, User
from django.urls import reverse
from django.db.models import *
from django.contrib.postgres.aggregates import *
from django.utils import dateparse

from ajax_datatable.views import AjaxDatatableView
from datetime import date, datetime, time, timedelta

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
        {'name': 'Agent Dashboard', 'visible': True, 'searchable': False, },
    ]

    def customize_row(self, row, obj):
        row['Agent Dashboard'] = '<a class="btn btn-primary btn-sm btn-block" href="%s">View</a>' % (
            reverse('agent_page', args=(obj.id,))
        )

    def get_initial_queryset(self, request=None):

        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.filter(user__is_superuser=False)

        return queryset


class AgentContactsAjaxDatatableView(AjaxDatatableView):

    model = ReqService
    title = 'ReqService'
    initial_order = [["contact_id_id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'contact_id_id', 'visible': True, },
    ]

    def get_initial_queryset(self, request=None):

        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.filter(contact_id_id__agent=request.REQUEST.get('agent'))

        return queryset

