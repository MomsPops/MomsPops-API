from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Notification, NotificationAccount


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Representation of notifications in admin interface.
    """

    list_display = ('text', 'links')
    search_fields = ('text', 'account__user__username')


@admin.register(NotificationAccount)
class NotificationAccountAdmin(admin.ModelAdmin):
    """
    Representation of notifications in admin interface.
    """

    list_display = ('account', 'notification', 'viewed')
    search_fields = ('account__user__username', 'notification__text')
    list_filter = ('viewed',)
    raw_id_fields = ('account', 'notification')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.select_related(
            "notification",
            "account__user"
        )
