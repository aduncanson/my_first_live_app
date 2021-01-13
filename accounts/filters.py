import django_filters
from django_filters import DateFilter, CharFilter, DateTimeFilter
from django import forms

from .models import *

from datetime import datetime

"""
    Returns filtered queryset depending on POSTed inputs
    Now decomissioned as using responsive filter in tables rather than POSTed fields
"""
class AgentListFilter(django_filters.FilterSet):
    username = CharFilter(field_name="user_id__username", lookup_expr="icontains")
    team = CharFilter(field_name="team_id__team_name", lookup_expr="icontains")
    department = CharFilter(field_name="team_id__department_id__department_name", lookup_expr="icontains")

    class Meta:
        model = Agent
        fields = []
