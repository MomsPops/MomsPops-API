from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
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
