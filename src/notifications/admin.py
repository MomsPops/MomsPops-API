from django.contrib import admin

from .models import Notification, NotificationAccount


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Representation of notifications in admin interface.
    """
    list_display = ('text', 'link', "sender")
    search_fields = ('text', 'account__user__username')


@admin.register(NotificationAccount)
class NotificationAccountAdmin(admin.ModelAdmin):
    """
    Representation of notifications in admin interface.
    """
    list_display = ('notification', 'account', "viewed")
