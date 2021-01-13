# existing django imports
from django.db.models import *
from django.contrib.postgres.aggregates import *
# my django imports
from ..models import *

"""
    Returns a dict of the statistics used on report pages e.g. average call length, total contacts
"""
def statistic_banner(request, queryset):

    # Returns the user's criteria set
    agent_search = AgentSearch.objects.get(agent=request.user.agent)

    # Returns the statistics used in the upper banner of the template
    stats = queryset.values("grouper").annotate(
        # All contacts within queryset
        full_call_count=Count("contact_id", distinct=True),
        # All contacts within queryset that meet criteria
        criteria_call_count=Count(
            Case(
                When(
                    call_time__lte=agent_search.call_lower_limit,
                    contact_id__contact_session_id__brand_id__in=agent_search.brands.all(),
                    then=F("contact_id")
                    ),
                When(
                    call_time__gte=agent_search.call_upper_limit,
                    contact_id__contact_session_id__brand_id__in=agent_search.brands.all(),
                    then=F("contact_id")
                    ),
                output_field=IntegerField(),
            ),
            distinct=True
        ),
        # Average call duration
        call_average=Avg("call_time", distinct=True),
    )

    # Dict to be returned
    context = {
        "full_call_count": stats.values("full_call_count")[0]["full_call_count"],
        "criteria_call_count": stats.values("criteria_call_count")[0]["criteria_call_count"],
        "call_average": stats.values("call_average")[0]["call_average"],
    }

    return context
