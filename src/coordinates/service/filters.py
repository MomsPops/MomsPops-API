from datetime import datetime, timezone, timedelta
from django.conf import settings

from .calculations import calculate_vector_distance, vectorize_queryset_dict


def filter_time(queryset, time_delta_limit):
    """Return generator yielding coords filtered by time."""
    now_time = datetime.now(tz=timezone.utc)
    for q in queryset:
        if now_time - datetime.strptime(q['time'], settings.TIME_FORMAT) <= time_delta_limit:
            yield q


def filter_distance(coord, queryset, distance_limit: int):
    """Return generator yielding coords filtered by distance."""
    lat_v, lon_v = vectorize_queryset_dict(queryset)
    vector_distance = calculate_vector_distance(
        lat1=coord['lat'],
        lon1=coord['lon'],
        lat2=lat_v,
        lon2=lon_v
    )
    for d, q in zip(vector_distance, queryset):
        if d <= distance_limit:
            yield d, q


def filter_coordinates(
        coord: dict,
        queryset: list[dict],
        time_delta_limit=timedelta(minutes=10),
        distance_limit: int = 3000
):
    """Return generator yielding coords both filtered by time and distance."""
    time_filtered_queryset_generator = filter_time(queryset=queryset, time_delta_limit=time_delta_limit)
    yield from filter_distance(
        queryset=time_filtered_queryset_generator,
        coord=coord,
        distance_limit=distance_limit
    )
