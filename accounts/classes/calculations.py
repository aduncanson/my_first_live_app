# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *


def dailyStats(request, queryset):

    agent_search = AgentSearch.objects.get(agent=request.user.agent)

    stats = queryset.values("grouper").annotate(
        full_call_count=Count("contact_id", distinct=True),
        criteria_call_count=Count(
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
        call_average=Avg("call_time", distinct=True),
    )

    context = {
        "full_call_count": stats.values("full_call_count")[0]["full_call_count"],
        "criteria_call_count": stats.values("criteria_call_count")[0]["criteria_call_count"],
        "call_average": stats.values("call_average")[0]["call_average"],
    }

    return context
