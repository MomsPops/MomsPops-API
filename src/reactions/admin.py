from django.contrib import admin

from .models import ReactionItem


@admin.register(ReactionItem)
class ReactionItemeModel(admin.ModelAdmin):
    list_display = ("id",)
