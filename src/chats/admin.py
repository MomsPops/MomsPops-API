from django.contrib import admin
from .models import Chat, ChatMessage, Group, GroupMessage, Message, MessageMediaFile


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """
    Representation of chats in admin interface.
    """
    list_display = ('time_created',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Representation of groups in admin interface.
    """
    list_display = ('title', 'owner', 'time_created')
    search_fields = ('owner__user__username', 'meeting_time', 'location_coordinate')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Representation of messages in admin interface.
    """
    list_display = ('account', 'text', 'available')
    search_fields = ('account__user__username', 'text')


@admin.register(MessageMediaFile)
class MessageMediaFileAdmin(admin.ModelAdmin):
    """
    Representation of messages media files in admin interface.
    """
    list_display = ('time_created',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Representation of messages in chats in admin interface.
    """
    list_display = ('message',)


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    """
    Representation of messages in groupss in admin interface.
    """
    list_display = ('group', 'message')
    search_fields = ('group',)
