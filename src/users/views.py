from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from http import HTTPStatus

from .permissions import IsToAccount, IsFromAccount
from .serializers import (
    AccountCreateSerializer, AccountDetailSerializer, UserCreateSerializer,
    BlockUserCreateSerializer, PasswordResetSerializer,
    FriendshipRequestCreateSerializer, FriendshipRequestListSerializer

)
from .models import Account, User, FriendshipRequest
from .service.email import send_email, decode_uid, check_activation_token
from rest_framework.decorators import action


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def get_permissions(self):
        if self.action == "create" or self.action == "password_reset":
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

    @action(detail=False, methods=['post'], serializer_class=PasswordResetSerializer)
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        username = validated_data.get('username')
        password = validated_data.get('password')
        new_password = validated_data.get('new_password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=HTTPStatus.BAD_REQUEST)
        if not user.check_password(password):
            return Response({'message': 'Incorrect username or password'}, status=HTTPStatus.BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=HTTPStatus.OK)


@api_view(['GET'])
def user_activation_api_view(request, uid, token):
    user = get_object_or_404(User, pk=decode_uid(uid))
    if check_activation_token(user=user, token=token):
        Account.objects.activate(instance=user.account)
    return redirect(reverse("token_obtain"))


class BlackListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Account.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return AccountDetailSerializer(*args, **kwargs)
        elif self.action == "create":
            return BlockUserCreateSerializer(*args, **kwargs)
        elif self.action == "destroy":
            return BlockUserCreateSerializer(*args, **kwargs)
        else:
            assert True

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data['username'] == request.user.username:
            return Response(
                {"detail": "You cannot add yourself to a black list"},
                status=HTTPStatus.BAD_REQUEST
            )
        Account.objects.block_user(
            account=request.user.account,
            username=serializer.data['username']
        )
        return Response(
            {"detail": "User blocked successfully."},
            status=HTTPStatus.OK
        )

    def list(self, request, *args, **kwargs):
        black_list = request.user.account.black_list.all()
        serializer = self.get_serializer(instance=black_list, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data['username'] == request.user.username:
            return Response(
                {"detail": "You cannot remove yourself from a black list"},
                status=HTTPStatus.BAD_REQUEST
            )
        Account.objects.unblock_user(
            account=request.user.account,
            username=serializer.data['username']
        )
        return Response(
            {"detail": "User unblocked successfully."},
            status=HTTPStatus.OK
        )


class FriendshipViewSet(viewsets.GenericViewSet):
    """Friendship view set."""
    queryset = FriendshipRequest.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "friendship_request_id"

    def get_permissions(self) -> list:
        permission_classes = [IsAuthenticated]
        if self.action == "update":
            permission_classes.append(IsToAccount)
        elif self.action == "destroy":
            permission_classes.append(IsFromAccount)
        return [pc() for pc in permission_classes]

    def get_serializer_context(self) -> dict:
        return {
            "request": self.request
        }

    def list(self, request):
        incoming_requests_serializer = FriendshipRequestListSerializer(
            request.user.account.incoming_requests, many=True
        )
        outcoming_requests_serializer = FriendshipRequestListSerializer(
            request.user.account.outcoming_requests, many=True
        )
        return Response(
            {
                "incoming": incoming_requests_serializer.data,
                "outcoming": outcoming_requests_serializer.data
            }
        )

    def create(self, request) -> Response:
        serializer = FriendshipRequestCreateSerializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        detail_serializer = FriendshipRequestListSerializer(obj)
        return Response(detail_serializer.data)

    def update(self, request, friendship_request_id: str) -> Response:
        friendship_request = self.get_object()
        self.check_object_permissions(request, friendship_request)
        friendship_request.accept()
        return Response({"detail": "Friend request is accepted successfully."})

    def destroy(self, request, friendship_request_id: str) -> Response:
        friendship_request = self.get_object()
        self.check_object_permissions(request, friendship_request)
        friendship_request.delete()
        return Response({"detail": "Friend request is deleted successfully."})
