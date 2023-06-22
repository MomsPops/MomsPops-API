from django.contrib import admin

from .models import City, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
