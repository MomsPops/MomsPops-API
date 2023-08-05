from rest_framework.permissions import BasePermission


class IsToAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account == obj.to_account


class IsFromAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account == obj.form_account
