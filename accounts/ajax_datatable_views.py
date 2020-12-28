from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent list'
    initial_order = [["user", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        #AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'user2', 'visible': True, },
        {'name': 'team_id', 'visible': True, },
        {'name': 'Department Id', 'foreign_field': 'team_id__department_id', 'visible': True, },
    ]
