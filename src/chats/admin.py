from django.contrib import admin
from .models import Chat, Group, Message, MessageMedia


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """
    Representation of chats in admin interface.
    """
    list_display = ('id', 'time_created')
    list_filter = ('type',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Representation of groups in admin interface.
    """
    list_display = ('title', 'owner', 'time_created')
    search_fields = ('owner__user__username', 'coordinate')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Representation of messages in admin interface.
    """
    list_display = ('account', 'text', 'viewed')
    search_fields = ('account__user__username', 'text')


@admin.register(MessageMedia)
class MessageMediaAdmin(admin.ModelAdmin):
    """
    Representation of messages media files in admin interface.
    """
    list_display = ('time_created', "media", "extension")
