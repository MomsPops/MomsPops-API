from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = User.create(**serializer.validated_data)
        if user is None:
            return Response({"detail": "Data is invalid"})

        return Response({'user': serializer.validated_data})

    @action(methods=["GET"], detail=True,
            url_name="is_active", url_path='is-active')
    def is_active(self, request):
        is_active = request.user


