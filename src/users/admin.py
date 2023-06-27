from django.contrib import admin

from .models import Account, SocialNetworkLink


class SocialNetworkLinkInline(admin.TabularInline):
    extra = 1
    model = SocialNetworkLink


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (SocialNetworkLinkInline,)

    list_display = ("user", "city", "status")
    list_filter = ["city", "tags"]
    search_fields = ["bio", "status", "birthday"]
    list_editable = ["status", "city"]
