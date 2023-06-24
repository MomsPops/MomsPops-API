from rest_framework.permissions import BasePermission

from .models import Profile


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Profile):
        return request.user.account == obj.account
