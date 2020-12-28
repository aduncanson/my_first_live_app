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
        {'name': 'user_id', 'visible': True, },
        {'name': 'team_id_id', 'visible': True, },
        {'name': 'first_name', 'foreign_field': 'user_id__first_name', 'visible': True, },
    ]
