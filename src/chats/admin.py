from django.contrib import admin
from .models import Chat, ChatMessage, Group, GroupMessage, Message, MessageMediaFile


class ChatAdmin(admin.ModelAdmin):
    """
    Representation of chats in admin interface.
    """

    list_display = ('type',)
    list_filter = ('type',)


class GroupAdmin(admin.ModelAdmin):
    """
    Representation of groups in admin interface.
    """

    list_display = ('title', 'owner')
    search_fields = ('owner__user__username', 'meeting_time', 'location_coordinate')


class MessageAdmin(admin.ModelAdmin):
    """
    Representation of messages in admin interface.
    """

    list_display = ('account', 'text', 'available')
    search_fields = ('account__user__username', 'text')


class MessageMediaFileAdmin(admin.ModelAdmin):
    """
    Representation of messages media files in admin interface.
    """

    search_fields = ('message__account__user__username', 'message__text')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ChatMessage)
admin.site.register(GroupMessage)
admin.site.register(MessageMediaFile, MessageMediaFileAdmin)
