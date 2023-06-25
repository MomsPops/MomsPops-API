from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Coordinate
from .serializer import CoordinateCreateSerializer, CoordinateListSerializer


class CoordinateCreateAPIView(generics.CreateAPIView):
    queryset = Coordinate.object.all()
    serializer_class = CoordinateCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.coordinate.object.update(**serializer.validated_data)
        return Response(serializer.validated_data)


class CoordinateNearAPIView(generics.ListAPIView):
    queryset = Coordinate.object.all()
    serializer_class = CoordinateListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_coordinate = request.user.coordinate
        near_coordinates = Coordinate.coordinate_manager.all_near(user_coordinate)
        return self.get_serializer_class()(near_coordinates, many=True)
