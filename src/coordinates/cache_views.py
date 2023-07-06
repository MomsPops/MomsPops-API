from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from datetime import datetime
from datetime import timezone

from .validators import validate_latitude, validate_longitude
from .service.filters import filter_coordinates


@api_view(["POST"])
def set_coordinate(request):
    if request.user.is_authenticated:
        if 'lat' in request.data and 'lon' in request.data:
            try:
                lat = validate_latitude(lat=request.data['lat'])
                lon = validate_longitude(lon=request.data['lon'])
                cache.set(
                    request.user.username,
                    {
                        'lat': int(lat),
                        "lon": int(lon),
                        "time": datetime.now(tz=timezone.utc).strftime(settings.TIME_FORMAT)
                    }
                )
                return Response("Successfully set coordinate", status=200)
            except ValidationError as e:
                return Response(str(e), status=400)
        else:
            return Response("Data should contain `lat` and `lon` values.", status=400)
    else:
        return Response("No permission to watch this data.", status=403)


@api_view(["DELETE"])
def delete_coordinate(request):
    if request.user.is_authenticated:
        cache.delete(request.user.username)
        return Response("Successfully deleted coordinate", status=200)
    else:
        return Response("No permission to watch this data.", status=403)


@api_view(['GET'])
def get_near_coordinates(request):
    if request.user.is_authenticated:
        user_coordinate = cache.get(request.user.username)
        if user_coordinate is not None:
            coordinates_keys = cache.keys("*")
            return Response(
                data=[
                    {
                        # "lat": query['lat'],
                        # "lon": query['lon'],
                        "profile_url": reverse("profiles_detail", kwargs={'username': query['distance']}),
                        "distance": distance,
                        "user_coordinate": user_coordinate
                    }
                    for distance, query in filter_coordinates(
                        coord=user_coordinate,
                        queryset=[cache.get(key) for key in coordinates_keys]
                    )
                ],
                status=200
            )
        else:
            return Response("User has no coordinate", status=400)
    else:
        return Response("No permission to watch this data.", status=403)
