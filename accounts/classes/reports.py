# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *
from ..forms import *
# from ..filters import *
from ..decorators import *
from ..tables import *

# external imports
from datetime import datetime


def full_agent_contact(agent, start_date, end_date):

    calls_today = ReqService.objects.filter(
        contact_id_id__contact_date__gte=start_date,
        contact_id_id__contact_date__lte=end_date,
        contact_id_id__agent_id=agent.user
    )

    return calls_today


def criteria_agent_contact(agent, report):

    agent_search = AgentSearch.objects.get(agent=agent)

    report_annotated = report.annotate(
        call_time=F('contact_id_id__contact_session_id_id__call_end_time') - F('contact_id_id__contact_session_id_id__call_start_time')
    )

    report_annotated = report_annotated.values(
            "contact_id",
            "contact_id__contact_date",
            "call_time",
            "contact_id__contact_session_id__call_start_time",
            "contact_id__contact_session_id__wrap_up_duration",
            "contact_id__contact_session_id__call_end_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
    ).annotate(
        demo=type(ArrayAgg('service_type_id__service_type_name', ordering=("req_service_id")))
    )

    report_annotated_filter = report_annotated.filter(
        call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
        contact_id_id__contact_session_id__brand_id__in=agent_search.brands.all()
    ).order_by("contact_id")

    return report_annotated_filter
