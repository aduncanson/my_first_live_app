# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *
from ..forms import *
# from ..filters import *
from ..decorators import *
from ..tables import *


def agent_contact(agent, start_date, end_date):

    agent_search = AgentSearch.objects.get(agent=agent)

    all_services = ReqService.objects.filter(
        contact_id_id__contact_date__gte=start_date,
        contact_id_id__contact_date__lte=end_date,
        contact_id_id__agent_id=agent.user
    )

    all_calls = all_services.values(
            "contact_id",
            "contact_id__contact_date",
            "contact_id__contact_session_id__call_start_time",
            "contact_id__contact_session_id__wrap_up_duration",
            "contact_id__contact_session_id__call_end_time",
            "contact_id__call_outcome",
            "contact_id__wrap_up_notes",
    ).annotate(
        comments=ArrayAgg('comments', ordering=("req_service_id")),
        services=ArrayAgg('service_type_id__service_type_name', ordering=("req_service_id"))
    )

    all_calls_with_ct = all_calls.annotate(
        call_time=F('contact_id_id__contact_session_id_id__call_end_time') - F('contact_id_id__contact_session_id_id__call_start_time')
    )

    criteria_calls_with_ct = all_calls_with_ct.filter(
        call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
        contact_id_id__contact_session_id__brand_id__in=agent_search.brands.all()
    ).order_by("-call_time")

    content = {
        "all_calls_with_ct": all_calls_with_ct,
        "criteria_calls_with_ct": criteria_calls_with_ct
    }

    return content
