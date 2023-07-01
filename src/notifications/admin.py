from django.contrib import admin

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
    Representation of personal notifications in admin interface.
    """

    list_display = ('account', 'notification', 'viewed')
    search_fields = ('account__user__username', 'notification__text')
    list_filter = ('viewed',)
