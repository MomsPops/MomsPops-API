from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import EventsFilterSet
from .models import Event
from .permissions import OwnerOrReadOnly
from .serializers import EventCreateSerializer, EventDetailSerializer


class EventViewSet(ModelViewSet):
    """
    ViewSet for events.
    """
    permission_classes = (IsAuthenticated, OwnerOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = EventsFilterSet

    def get_permissions(self):
        super().get_permissions()
        if self.action == 'create':
            return [IsAuthenticated()]
        return [OwnerOrReadOnly()]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['create', 'update']:
            return EventCreateSerializer
        return EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.account)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user.account)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.time_finished < timezone.now():
            return Response({"error": "Нельзя изменить прошедшее событие."})
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        group = event.group
        if (event.time_finished > timezone.now()) & (len(event.group.members.all()) == 1):
            group.delete()
            return super().destroy(request, *args, **kwargs)
        return Response({"error": "Нельзя удалить прошедшее событие."})
