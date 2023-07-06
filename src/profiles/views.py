from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Profile, Post
from .serializers import (
    ProfileListSerializer, ProfileDetailSerializer,
    PostDetailSerializer, PostListSerializer, PostCreateSerializer
)
from .permissions import IsProfileOwner, IsPostOwner


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "username"
    lookup_field = "account__user__username"

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return ProfileListSerializer(*args, **kwargs)
        elif self.action == "posts":
            return PostListSerializer(*args, **kwargs)
        else:
            return ProfileDetailSerializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ("list", "retrieve", "posts"):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsProfileOwner]
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
