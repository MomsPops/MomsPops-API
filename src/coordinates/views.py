from rest_framework import generics, views, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CoordinateCreateSerializer, CoordinateListSerializer
from .models import Coordinate


class CoordinateViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Create and destroy current user coordinate.
    """
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            coordinate = Coordinate.coordinate_manager.get(source=request.user.account)
            coordinate.lat = serializer.validated_data['lat']
            coordinate.lon = serializer.validated_data['lon']
            coordinate.save()
        except ObjectDoesNotExist:
            coordinate = Coordinate.coordinate_manager.create(
                **serializer.validated_data, source=request.user.account
            )
        return Response(serializer.validated_data, status=201)

    def destroy(self, request, *args, **kwargs):
        request.user.account.coordinate.delete()
        return Response({"detail": "Coordinate deleted."})


class CoordinateDecodeAPIView(views.APIView):
    """
    Represents current user coordinate to place (city, street, .etc)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_coordinate = request.user.account.coordinate
        if user_coordinate is None:
            return Response({"detail": "There is no coordinate to decode."}, status=404)
        return Response({"place": Coordinate.coordinate_manager.decode(user_coordinate)})


class CoordinateNearAPIView(generics.ListAPIView):
    """
    Get all near user for the current_user
    """
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_coordinate = request.user.account.coordinate
        if user_coordinate is None:
            return Response({"detail": "Cannot find current coordinate."}, status=404)
        near_coordinates = Coordinate.coordinate_manager.all_near(user_coordinate)
        return Response(self.get_serializer_class()(near_coordinates, many=True))
