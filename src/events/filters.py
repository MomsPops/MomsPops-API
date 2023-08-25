from django.utils import timezone
from django_filters import (CharFilter, DateTimeFromToRangeFilter, FilterSet,
                            TypedChoiceFilter)

from .models import Event

BOOLEAN_CHOICES = ((0, False), (1, True),)


class EventsFilterSet(FilterSet):
    """
    Filters for events.
    """
    creator = CharFilter(field_name='creator__user__username', lookup_expr='icontains')
    title = CharFilter(lookup_expr='icontains')
    event_start_time = DateTimeFromToRangeFilter(field_name='time_started')
    is_active = TypedChoiceFilter(choices=BOOLEAN_CHOICES,
                                  method='get_is_actives')
    is_ongoing = TypedChoiceFilter(choices=BOOLEAN_CHOICES,
                                   method='get_is_ongoings')

    class Meta:
        model = Event
        fields = ['creator', 'title', 'time_started']

    def get_is_actives(self, queryset, name, value):
        return queryset.filter(time_finished__gte=timezone.now())

    def get_is_ongoings(self, queryset, name, value):
        return queryset.filter(time_started__gte=timezone.now(),
                               time_finished__lte=timezone.now())
