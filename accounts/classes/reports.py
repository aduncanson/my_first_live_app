# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *
from ..forms import *
# from ..filters import *
from ..decorators import *
from ..tables import *

import datetime


def contact_reports(request, agent, start_date, end_date):

    agent_search = AgentSearch.objects.get(agent=request.user.agent)

    all_reqservices = ReqService.objects.filter(
        contact_id__contact_date__gte=start_date,
        contact_id__contact_date__lte=end_date,
        contact_id__agent_id=agent.user
    )

    full_contact_table = all_reqservices.values(
        "contact_id",
        "contact_id__contact_date",
        "contact_id__call_outcome",
        "contact_id__wrap_up_notes",
        "contact_id__contact_session_id__call_start_time",
        "contact_id__contact_session_id__wrap_up_duration",
        "contact_id__contact_session_id__call_end_time",
        "contact_id__contact_session_id__call_type",
        "contact_id__contact_session_id__dialled",
        "contact_id__contact_session_id__brand_id__brand_name",
    ).annotate(
        comments=ArrayAgg('comments', ordering=("req_service_id")),
        services=ArrayAgg('service_type_id__service_type_name', ordering=("req_service_id")),
        call_time=F('contact_id__contact_session_id__call_end_time') - F('contact_id__contact_session_id__call_start_time'),
    )

    criteria_contact_table = full_contact_table.filter(
        call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
        contact_id__contact_session_id__brand_id__in=agent_search.brands.all()
    )

    call_time_qs = all_reqservices.values(
        "contact_id__call_outcome",
    ).annotate(
        call_time=F('contact_id__contact_session_id__call_end_time') - F('contact_id__contact_session_id__call_start_time'),
    )

    call_outcome_table = call_time_qs.values(
        "contact_id__call_outcome",
    ).annotate(
        full_count=Count("contact_id", distinct=True),
        criteria_count=Count(
            Case(
                When(
                    call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
                    contact_id__contact_session_id__brand_id__in=agent_search.brands.all(),
                    then=F("contact_id")
                    ),
            output_field=IntegerField(),
        ),
        distinct=True
        ),
        max=Max("call_time"),
        avg=Avg("contact_id", distinct=True),
        min=Min("call_time"),
    )

    services_table = call_time_qs.values(
        "service_type_id__service_type_name",
    ).annotate(
        full_count=Count("req_service_id"),
        criteria_count=Count(
            Case(
                When(
                    call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
                    contact_id__contact_session_id__brand_id__in=agent_search.brands.all(),
                    then=F("contact_id")
                    ),
            output_field=IntegerField(),
        ),
        distinct=True
        ),
        max=Max("call_time"),
        avg=Avg("contact_id", distinct=True),
        min=Min("call_time"),
    )

    content = {
        "criteria_contact_table": criteria_contact_table,
        "call_outcome_table": call_outcome_table,
        "services_table": services_table,
    }

    return content
