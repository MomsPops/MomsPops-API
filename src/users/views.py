from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .serializers import AccountCreateSerializer, AccountDetailSerializer
from .models.account import Account


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_account = Account.objects.create_account(**request.data)
        return Response(AccountDetailSerializer(new_account).data)
