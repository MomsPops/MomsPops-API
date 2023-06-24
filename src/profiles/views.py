from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileListSerializer, ProfileDetailSerializer
from .permissions import IsProfileOwner


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    lookup_url_kwarg = "username"
    lookup_field = "account__user__username"

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return ProfileListSerializer(*args, **kwargs)
        else:
            return ProfileDetailSerializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            perm_classes = [IsAuthenticated]
        else:
            perm_classes = [IsAuthenticated, IsProfileOwner]
        return [pc() for pc in perm_classes]

    def update(self, request, *args, **kwargs):
        instance = Profile.objects.get(account__user__username=kwargs[self.lookup_url_kwarg])
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.update(instance, serializer.validated_data)
        serializer.save()
        instance.save()
        return Response(serializer.data, status=200)
