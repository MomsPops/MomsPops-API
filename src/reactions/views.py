from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from reactions.models import ReactionLike, ReactionItem
from reactions.serializers import ReactionItemSerializer, ReactionSerializer


class ReactionItemViewSet(viewsets.ModelViewSet):
    queryset = ReactionItem.objects.all()
    serializer_class = ReactionItemSerializer
    permission_classes = [IsAdminUser]


class ReactionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ReactionLike.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]
