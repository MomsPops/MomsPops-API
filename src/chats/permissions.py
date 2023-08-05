from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsChatMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.account.chats.all()


class IsGroupMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.account.groups.all()


def check_is_group_owner(account, group):
    if account != group.owner:
        raise PermissionDenied("You are not the owner.")


def check_is_group_public(group):
    if not group.is_public:
        raise PermissionDenied("Group is not private.")
