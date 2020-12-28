from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission, User

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = User
    title = 'User'
    initial_order = [["username", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'username', 'visible': True, },
        {'name': 'agent', 'foreign_field': 'user__agent', 'visible': True, },
    ]
