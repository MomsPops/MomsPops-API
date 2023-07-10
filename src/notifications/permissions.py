from rest_framework import permissions


class RecepientOnlyPermission(permissions.BasePermission):
    """Access only for notification's recipient."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.account == request.user.account
