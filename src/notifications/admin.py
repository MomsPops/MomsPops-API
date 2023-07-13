from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Representation of notifications in admin interface.
    """
    list_display = ('text', 'links', "sender")
    search_fields = ('text', 'account__user__username')
