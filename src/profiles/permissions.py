from rest_framework.permissions import BasePermission

from .models import Profile, Post


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Profile) -> bool:
        return request.user.account == obj.account   # type: ignore


class IsPostOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Post) -> bool:
        return request.user.account == obj.profile.account   # type: ignore
