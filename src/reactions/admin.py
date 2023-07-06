from django.contrib import admin

from .models import ReactionItem


@admin.register(ReactionItem)
class ReactionItemModel(admin.ModelAdmin):
    list_display = ("id",)
