from django.contrib import admin

from .models import Profile, Post, Tag, SocialNetworkLink


class SocialNetworkLinkInline(admin.TabularInline):
    extra = 1
    model = SocialNetworkLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (SocialNetworkLinkInline,)

    list_display = ("account", "status")
    list_filter = ["tags"]
    search_fields = ["bio", "status", "birthday"]
    list_editable = ["status"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "profile")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
