from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from .models import User


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        else:
            return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.user_objects.create(**serializer.validated_data)
        return Response({'user': serializer.validated_data})

