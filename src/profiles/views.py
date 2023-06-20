from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Profile, Note
from .serializers import (ProfileListSerializer, ProfileCreateSerializer, ProfileDetailSerializer,
                          NoteListSerializer, NoteDetailSerializer, NoteCreateSerializer)
from .permissions import IsOwner


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = "user__username"

    def get_permissions(self):
        if self.action in ("update", "destroy"):
            permission_classes = (IsOwner, )
        else:
            permission_classes = (IsAuthenticated, )
        return [pc() for pc in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializer
        elif self.action == 'detail':
            return ProfileDetailSerializer
        elif self.action == 'create':
            return ProfileCreateSerializer
        # else ?
        return ProfileDetailSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(
            instance=Profile.objects.get_all_active(),
            many=True
        )
        return Response(serializer.data)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', ):
            return NoteListSerializer
        if self.action == "create":
            return NoteCreateSerializer
        # else ?
        return NoteDetailSerializer

    def get_permissions(self):
        if self.action in {"update", "delete"}:
            permission_classes = (IsOwner, )
        else:
            permission_classes = (IsAuthenticated, )
        return [pc() for pc in permission_classes]

    def list(self, request, *args, **kwargs):
        username = kwargs.get('username')
        serializer = self.get_serializer_class()(
            instance=Note.objects.get_by_username(username),
            many=True
        )
        return Response(serializer.data)



