from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission


class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent list'
    initial_order = [["user", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'user', 'visible': False, },
        {'name': 'user.first_name', 'visible': True, },
        {'name': 'user.last_name', 'visible': True, },
        {'name': 'user.email', 'visible': True, },
        {'name': 'team_idel', 'visible': True, },
        {'name': 'team_id.department_id', 'visible': True, },
    ]
