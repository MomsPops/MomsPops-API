from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Region
from .serializers import LocationListSerializer
from .service.dump_data import dump_locations, dump_regions, dump_cities


class LocationListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = LocationListSerializer


class LocationLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        dump_locations()
        return Response({"detail": "Locations` data loaded successfully."})


class RegionLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        dump_regions()
        return Response({"detail": "Regions` data loaded successfully."})


class CityLoadDataAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        dump_cities()
        return Response({"detail": "Cities` data loaded successfully."})
