from django.contrib import admin

from .models import Account, User, FriendshipRequest


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "city")
    list_filter = ["city"]
    list_editable = ["city"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "to_account", "from_account")
