import django_filters
from django_filters import DateFilter, CharFilter, DateTimeFilter
from django import forms

from .models import *

from datetime import datetime

class AgentFilter(django_filters.FilterSet):
    start_date = DateTimeFilter(field_name="contact_date", lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    end_date = DateTimeFilter(field_name="contact_date", lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    wrap_up_notes = CharFilter(field_name="wrap_up_notes", lookup_expr="icontains")
    call_outcome = CharFilter(field_name="call_outcome", lookup_expr="icontains")

    class Meta:
        model = ClientContact
        fields = []

class AgentListFilter(django_filters.FilterSet):
    username = CharFilter(field_name="user_id__username", lookup_expr="icontains")
    team = CharFilter(field_name="team_id__team_name", lookup_expr="icontains")
    department = CharFilter(field_name="team_id__department_id__department_name", lookup_expr="icontains")

    class Meta:
        model = Agent
        fields = []
