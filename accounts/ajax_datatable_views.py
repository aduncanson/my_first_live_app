from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Permission
    title = 'Permissions'
    initial_order = [[1, "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'codename', 'visible': True, },
    ]
