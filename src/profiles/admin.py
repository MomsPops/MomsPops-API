from django.contrib import admin

from .models import SocialNetworkLink, Profile, Post, Tag


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "account")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "profile")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(SocialNetworkLink)
class SocialNetworkLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "profile", "link")
