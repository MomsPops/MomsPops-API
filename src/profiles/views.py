from http import HTTPStatus

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Account
from .models import Profile, Post
from .serializers import (
    ProfileListSerializer, ProfileDetailSerializer,
    PostDetailSerializer, PostListSerializer, PostCreateSerializer
)
from users.serializers import AccountDetailSerializer
from .permissions import IsProfileOwner, IsPostOwner


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "username"
    lookup_field = "account__user__username"

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        data = serializer.data
        data['is_friend'] = profile.account in request.user.account.friends.all()
        if not data["is_friend"]:
            data['is_outcoming'] = request.user.account.outcoming_requests.filter(to_account=profile.account).exists()
            data['is_incoming'] = request.user.account.incoming_requests.filter(to_account=profile.account).exists()
        return Response(data)

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            serializer = ProfileListSerializer
        elif self.action == "posts":
            serializer = PostListSerializer
        elif self.action == "friends":
            serializer = AccountDetailSerializer
        else:
            serializer = ProfileDetailSerializer
        return serializer(*args, **kwargs)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ("partial_update", "update", "friends_delete"):
            permission_classes.append(IsProfileOwner)
        return [pc() for pc in permission_classes]

    def update(self, request, *args, **kwargs):
        instance = Profile.objects.get(account__user__username=kwargs[self.lookup_url_kwarg])
        self.check_object_permissions(request, obj=instance)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.update(instance, serializer.validated_data)
        serializer.save()
        instance.save()
        return Response(serializer.data, status=200)

    @action(methods=['get'], detail=True)
    def posts(self, request, username):
        posts = Post.post_manager.all_by_username(username)
        serializer = self.get_serializer(instance=posts, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def friends(self, request, username):
        profile = self.get_object()
        serializer = self.get_serializer(instance=profile.account.friends, many=True)
        return Response(serializer.data)

    @action(methods=['delete'], detail=True)
    def friend_delete(self, request, username):
        profile = self.get_object()
        if profile.account == request.user.account:
            return Response(
                {"detail": "Cannot delete yourself from friends."},
                status=HTTPStatus.BAD_REQUEST
            )
        elif profile.account not in request.user.account.friends.all():
            return Response(
                {"detail": f"Account {profile.account} is not your friend."},
                status=HTTPStatus.BAD_REQUEST
            )
        Account.objects.break_friendship(profile.account, request.user.account)
        return Response({"detail": "Friendship is broken successfully."})


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "retrieve":
            perm_classes = [IsAuthenticated]
        else:
            perm_classes = [IsAuthenticated, IsPostOwner]
        return [pc() for pc in perm_classes]

    def get_serializer(self, *args, **kwargs):
        if self.action == "detail":
            return PostDetailSerializer(*args, **kwargs)
        elif self.action == "create":
            return PostCreateSerializer(*args, **kwargs)
        else:
            return PostDetailSerializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        profile = request.user.account.profile
        data = dict(**request.data, profile=profile)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        Post.objects.create(**data)
        return Response(serializer.validated_data, status=201)

    def partial_update(self, request, *args, **kwargs):
        instance = Post.objects.get(id=kwargs[self.lookup_url_kwarg])
        self.check_object_permissions(request, obj=instance)    # check if request user is owner
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.update(instance, serializer.validated_data)
        serializer.save()
        instance.save()
        return Response({"data": instance.text}, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = Post.objects.get(id=kwargs[self.lookup_url_kwarg])
        self.check_object_permissions(request, obj=instance)    # check if request user is owner
        instance.delete()
        return Response({"Post was deleted successfully."})
