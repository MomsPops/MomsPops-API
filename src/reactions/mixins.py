from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reactions.serializers import FanSerializer
from reactions.services import add_like, remove_like, get_fans


class ReactionsdMixin:
    @action(detail=True, methods=['post'],
            url_path='like/(P<reaction_pk>[a-z0-9]+)',
            permission_classes=[AllowAny])
    def like(self, request, pk=None, reaction_pk=None):
        obj = self.get_object()
        reaction_id = self.kwargs['reaction_pk']
        add_like(obj, request.user, reaction_id)

        return Response()

    @action(detail=True, methods=['delete'], url_name='unlike',
            url_path='unlike/(?P<reaction_pk>[a-z0-9]+)',
            permission_classes=[AllowAny])
    def unlike(self, request, pk=None, reaction_pk=None):
        obj = self.get_object()
        reaction_id = self.kwargs['reaction_pk']
        remove_like(obj, request.user, reaction_id)
        return Response()

    @action(detail=True, methods=['get'], )
    def get_fans(self, request, pk=None, reaction_pk=None, permission_classes=[AllowAny]):
        obj = self.get_object()
        fans = get_fans(obj, request.user)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
