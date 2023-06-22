from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountMain(admin.ModelAdmin):
    list_display = ("user", "city")
