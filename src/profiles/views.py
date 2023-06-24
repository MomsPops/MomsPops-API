from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        else:
            return ProfileDetailSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            perm_classes = [IsAuthenticated]
        else:
            perm_classes = [IsAuthenticated, IsProfileOwner]
        return [pc() for pc in perm_classes]

