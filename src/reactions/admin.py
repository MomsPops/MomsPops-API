from django.contrib import admin

from .models import ReactionItem, Reaction


@admin.register(ReactionItem)
class ReactionItemAdmin(admin.ModelAdmin):
    list_display = ("name", "image")


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("owner", "item")
