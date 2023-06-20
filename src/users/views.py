from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserListSerializer, UserDetailSerializer
from .models import User


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "detail"):
            return UserDetailSerializer
        else:
            return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid()
        user = User.objects.create(**serializer.validated_data)
        if user is None:
            return Response({"detail": "Data is invalid"}, status=403)

        return Response({'user': serializer.validated_data})

    def update(self, request, *args, **kwargs):
        user = request.user
        print(user, request.headers)
        for k, v in request.data.items():
            setattr(user, k, v)

        user.save()
        serializer = self.get_serializer_class()(instance=user)
        return Response({'user': serializer.data})


