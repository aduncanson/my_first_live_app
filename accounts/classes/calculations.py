# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *


def calculations(request, queryset):

    agent_search = AgentSearch.objects.get(agent=request.user.agent)

    stats = queryset.annotate(
        full_count=Count("contact_id"),
        criteria_count=Count(
            Case(
                When(
                    call_time__range=[agent_search.call_lower_limit, agent_search.call_upper_limit],
                    contact_session_id__brand_id__in=agent_search.brands.all(),
                    then=F("contact_id")
                    ),
            output_field=IntegerField(),
        ),
        distinct=True
        ),
        avg=Avg("contact_id"),
    )

    return stats
