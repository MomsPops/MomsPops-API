from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "city")
    list_filter = ["city"]
    list_editable = ["city"]
