from django.contrib import admin

from .models import City, Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
