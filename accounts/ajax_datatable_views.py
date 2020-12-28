from ajax_datatable.views import AjaxDatatableView

from .models import *

class AgentListAjaxDatatableView(AjaxDatatableView):

    model = Agent
    title = 'Agent'
    #initial_order = [["user", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
