from django.contrib import admin
from .models import Chat, Group, Message, ChatMessage, GroupMessage


class ChatMessageInline(admin.StackedInline):
    extra = 1
    model = ChatMessage
    verbose_name = "Cообщение в чате"
    verbose_name_plural = "Cообщения в чате"


class GroupMessageInline(admin.StackedInline):
    extra = 1
    model = GroupMessage
    verbose_name = "Групповое сообщение"
    verbose_name_plural = "Групповые сообщения"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = (ChatMessageInline,)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = (GroupMessageInline,)
    list_display = ("title", "owner", "meeting_time")
