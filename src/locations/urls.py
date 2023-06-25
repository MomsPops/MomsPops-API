from django.urls import path

from .views import CityListAPIView

urlpatterns = [
    path("cities/", CityListAPIView.as_view(), name='locations_cities'),

]
