from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializer import ReactionItemSerializer, ReactionSerializer
from .models import ReactionItem, Reaction


class ReactionItemViewSet(viewsets.ModelViewSet):
    queryset = ReactionItem.objects.all()
    serializer_class = ReactionItemSerializer
    permission_classes = [IsAuthenticated]


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]
