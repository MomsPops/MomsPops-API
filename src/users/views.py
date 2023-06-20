from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from .models import User


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("detail", ):
            return UserDetailSerializer
        elif self.action in ("create", ):
            return UserCreateSerializer
        else:
            return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        return Response(self.get_serializer_class()(user).data)

    def update(self, request, *args, **kwargs):
        user = request.user
        for k, v in request.data.items():
            setattr(user, k, v)

        user.save()
        serializer = self.get_serializer_class()(instance=user)
        return Response({'user': serializer.data})


