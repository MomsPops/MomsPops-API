from django.contrib import admin

from .models import Coordinate


@admin.register(Coordinate)
class CoordinateModel(admin.ModelAdmin):
    list_display = ("id", "lat", "lon", "account", "last_time")
