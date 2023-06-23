from rest_framework import generics

from .models import City
from .serializer import CitiesListSerializer


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitiesListSerializer
