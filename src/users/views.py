from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

from .serializers import (
    AccountCreateSerializer, AccountDetailSerializer, UserCreateSerializer,

)
from .models import Account, User
from .service.email import send_email, decode_uid, check_activation_token


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            perm_classes = [AllowAny]
        else:
            perm_classes = [IsAuthenticated]
        return [pc() for pc in perm_classes]

    def create(self, request, *args, **kwargs):
        """Create both user and account."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_account = Account.objects.create_account(**request.data)
        send_email(
            request=request,
            user=new_account.user
        )
        return Response(f"Activation link is send to {new_account.user.email}", status=201)

    def retrieve(self, request, *args, **kwargs):
        """Return current user account data."""
        serializer = AccountDetailSerializer(request.user.account)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update account or account and user together. Data is given
        as on account creation, but partial.
        """
        data = dict(**request.data)
        if "user" in data:
            user_serializer = UserCreateSerializer(instance=request.user, data=data['user'], partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.update(request.user, user_serializer.validated_data)
            data.pop('user')

        serializer = self.serializer_class(instance=request.user.account, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.account, serializer.validated_data)

        return Response(serializer.validated_data)

    def destroy(self, request, *args, **kwargs):
        """
        If request body is empty, function deactivates user,
        else deletes current user instance.
        """
        if request.data:
            self.perform_destroy(request.user)
            return Response({"detail": "User deleted."})
        else:
            Account.objects.deactivate(request.user.account)
            return Response({"detail": "User deactivated."})


@api_view(['GET'])
def user_activation_api_view(request, uid, token):
    user = get_object_or_404(User, pk=decode_uid(uid))
    if check_activation_token(user=user, token=token):
        Account.objects.activate(instance=user.account)
    return redirect(reverse("token_obtain"))


# class BlockUserViewSet(mixins.ListModelMixin,
#                        mixins.CreateModelMixin,
#                        mixins.DestroyModelMixin,
#                        viewsets.GenericViewSet):
#     queryset = Account.objects.all()
#
#     def get_serializer(self, *args, **kwargs):
#         match self.action:  # type: ignore
#             case "list":
#                 return BlockUserListSerializer(*args, **kwargs)
#             case "create":
#                 return BlockUserCreateSerializer(*args, **kwargs)
#             case "destroy":
#                 return BlockUserCreateSerializer(*args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if serializer.validated_data['username'] == request.user.username:
#             return Response(
#                 {"detail": "You cannot add yourself to a black list"},
#                 status=400
#             )
#         Account.objects.block_user(
#             account=request.account,
#             username=serializer.validated_data['username']
#         )
#         return Response(
#             {"detail": "User blocked successfully."},
#             status=201
#         )
#
#     def list(self, request, *args, **kwargs):
#         black_list = request.user.account.black_list.all()
#         serializer = self.get_serializer(instance=black_list, many=True)
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if serializer.validated_data['username'] == request.user.username:
#             return Response(
#                 {"detail": "You cannot add yourself to a black list"},
#                 status=400
#             )
#         Account.objects.unblock_user(
#             account=request.account,
#             username=serializer.validated_data['username']
#         )
#         return Response(
#             {"detail": "User unblocked successfully."},
#             status=201
#         )
