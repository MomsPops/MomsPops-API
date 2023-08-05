from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Group
from .serializers import GroupListSerializer
from .filters import GroupFilter


class GroupViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return GroupListSerializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        filters = GroupFilter(data=request.GET, queryset=self.get_queryset())
        queryset = filters.qs
        distance = request.GET.get("distance")
        if distance is not None:
            if request.user.account.coordinate is None:
                return Response([])
            queryset = request.user.account.coordinate.__class__.coordinate_manager.all_near(
                source=request.user.account,
                distance=int(distance),
                queryset=queryset
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
