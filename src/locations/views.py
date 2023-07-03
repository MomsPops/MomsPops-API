from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Region
from .serializers import LocationListSerializer
from .service.load_data import load_locations, load_cities, load_regions
from .tasks import load_regions_task, load_cities_task, load_locations_task


class LocationListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = LocationListSerializer


class LocationLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        load_locations()
        return Response({"detail": "Locations` data loaded successfully."})


class RegionLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        load_regions()
        return Response({"detail": "Regions` data loaded successfully."})


class CityLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        load_cities()
        return Response({"detail": "Cities` data loaded successfully."})


@api_view(['POST'])
def load_locations_view(request):
    load_regions()
    load_cities_task.apply_async()
    return Response("Locations` data is started loading successfully.")


@api_view(['POST'])
def load_cities_view(request):
    load_cities_task.apply_async()
    return Response("Cities` data is started loading successfully.")


@api_view(['POST'])
def load_regions_view(request):
    load_regions_task.apply_async()
    return Response("Regions` data is started loading successfully.")
