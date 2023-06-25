from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import AccountCreateSerializer, AccountDetailSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            perm_classes = [AllowAny]
        else:
            perm_classes = [IsAuthenticated]
        return [pc() for pc in perm_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_account = Account.objects.create_account(**request.data)
        return Response(AccountDetailSerializer(new_account).data, status=201)

    def retrieve(self, request, *args, **kwargs):
        serializer = AccountDetailSerializer(request.user.account)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.account)
        serializer.update(**request.data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.data:
            self.perform_destroy(request.user)
            return Response({"detail": "User deleted."})
        else:
            Account.objects.deactivate(request.user.account)
            return Response({"detail": "User deactivated."})
