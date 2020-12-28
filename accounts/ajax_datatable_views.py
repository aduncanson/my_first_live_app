from ajax_datatable.views import AjaxDatatableView

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent'
    initial_order = [["Username", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'Username', 'foreign_field': 'user', 'visible': True, },
        {'name': 'First Name', 'foreign_field': 'user__first_name', 'visible': True, },
    ]
