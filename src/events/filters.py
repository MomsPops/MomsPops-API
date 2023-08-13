from datetime import datetime

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
    description = CharFilter(lookup_expr='icontains')
    event_start_time = DateTimeFromToRangeFilter(field_name='event_start_time')
    is_active = TypedChoiceFilter(choices=BOOLEAN_CHOICES,
                                  method='get_is_actives')
    is_ongoing = TypedChoiceFilter(choices=BOOLEAN_CHOICES,
                                   method='get_is_ongoings')

    class Meta:
        model = Event
        fields = ['creator', 'title', 'description', 'event_start_time']

    def get_is_actives(self, queryset, name, value):
        return queryset.filter(event_end_time__gte=datetime.now())

    def get_is_ongoings(self, queryset, name, value):
        return queryset.filter(event_start_time__gte=datetime.now(),
                               event_end_time__lte=datetime.now())
