from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from http import HTTPStatus
from .serializers import (
    AccountCreateSerializer, AccountDetailSerializer, UserCreateSerializer,
    BlockUserCreateSerializer, PasswordResetSerializer, PasswordResetPostSerializer,
    PasswordResetConfirmSerializer
)
from .models import Account, User
from .service.email import send_email, decode_uid, check_activation_token, send_password_reset_email
from rest_framework.decorators import action

from rest_framework.views import APIView

from rest_framework import status

import random


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response({'detail': 'Please register an account.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 8-digit random code and set it as the user's password reset token
        code = str(random.randint(10000000, 99999999))
        user.set_password(code)
        user.save()

        # Send the password reset email with the code
        send_password_reset_email(
                request=request,
                user=user,
                code=code
        )

        return Response({'detail': 'Password reset code sent to your email.'}, status=status.HTTP_201_CREATED)


class PasswordResetConfirmView(APIView):
    def put(self, request, *args, **kwargs):
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Decode the user ID from the code
        uid = request.user.id

        # Check if the code is valid and matches the user's password reset token
        user = User.objects.get(pk=uid)
        if not user.check_password(code):
            return Response({'detail': 'Invalid or expired code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if new_password and confirm_password match
        if new_password != confirm_password:
            return Response({'detail': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the user's password with the new password
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def get_permissions(self):
        if (self.action == "create" or
            self.action == "password_reset" or
            self.action == "password_reset_confirm" or
            self.action == "reset_password_request"):
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
    def reset_password(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['post'], serializer_class=PasswordResetPostSerializer)
    def reset_password_request(self, request, *args, **kwargs):
        # Создайте экземпляр PasswordResetRequestView
        reset_request_view = PasswordResetRequestView()

        # Вызовите метод post с передачей аргумента request
        return reset_request_view.post(request, *args, **kwargs)

    @action(detail=False, methods=['put'], serializer_class=PasswordResetConfirmSerializer)
    def reset_password_confirm(self, request, *args, **kwargs):
        reset_confirm_view = PasswordResetConfirmView.as_view()
        return reset_confirm_view(request, *args, **kwargs)


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
