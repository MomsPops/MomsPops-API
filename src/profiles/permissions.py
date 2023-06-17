from rest_framework.permissions import BasePermission


class HasProfile(BasePermission):
    def has_permission(self, request, view):
        try:
            profile = request.user.profile
            return True
        except:
            return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            profile = request.user.profile
            return obj.profile == profile
        except:
            return False
