from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile, Note
from .serializers import ProfileSerializer, NoteSerializer
from .permissions import HasProfile, IsOwner


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"

    def get_permissions(self):
        if self.action in ("update", ):
            permission_classes = (IsOwner, )
        else:
            permission_classes = (IsAuthenticated, )
        return [pc() for pc in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(Profile.objects.all(),
                                           many=True)
        return Response({"profiles": serializer})


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action in {"update", "delete"}:
            permission_classes = (IsOwner, )
        else:
            permission_classes = (IsAuthenticated, )
        return [pc() for pc in permission_classes]


