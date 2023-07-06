from django.contrib import admin

from .models import Account, User


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "city")
    list_filter = ["city"]
    list_editable = ["city"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
