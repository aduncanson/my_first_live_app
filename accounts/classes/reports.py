# existing django imports
from django.db.models import *
# my django imports
from ..models import *
from ..forms import *
# from ..filters import *
from ..decorators import *
from ..tables import *

# external imports
from datetime import datetime

def full_agent_contact(agent, start_date, end_date):

    calls_today = ClientContact.objects.filter(
        contact_date__gte=start_date,
        contact_date__lte=end_date,
        agent_id=agent
    )

    return calls_today


def criteria_agent_contact(agent, report):

    agent_search = AgentSearch.objects.get(agent=agent)

    report_annotated = report.annotate(
        call_time=F('contact_session_id_id__call_end_time') - F('contact_session_id_id__call_start_time')
    )

    report_annotated_filter = report_annotated.filter(
        call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
        contact_session_id__brand_id__in=agent_search.brands.all()
    ).order_by("contact_date")

    return report_annotated_filter
