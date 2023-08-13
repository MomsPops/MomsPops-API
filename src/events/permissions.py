from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrReadOnly(BasePermission):
    """
    Permission class for events.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.creator == request.user.account)
