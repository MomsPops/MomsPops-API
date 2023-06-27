from django.contrib import admin
from .models import Chat, Message, ChatType


class MessageInline(admin.TabularInline):
    fields = "account", "text", "img", "viewed", "reactions"
    extra = 1
    model = Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = (MessageInline,)
    list_display = ("type", "owner")


@admin.register(ChatType)
class ChatTypeAdmin(admin.ModelAdmin):
    pass
