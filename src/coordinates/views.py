from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import CoordinateCreateSerializer, CoordinateListSerializer
from .models import Coordinate


class CoordinatesViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Coordinate.object.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CoordinateCreateSerializer
        else:
            return CoordinateListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.coordinate.object.update(**serializer.validated_data)
        return Response(serializer.validated_data)

    @action(methods=['get'], detail=False)
    def all_near(self, request):
        user_coordinate = request.user.coordinate
        near_coordinates = Coordinate.coordinate_manager.all_near(user_coordinate)
        return self.get_serializer_class()(near_coordinates, many=True)
