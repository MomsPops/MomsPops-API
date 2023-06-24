from django.urls import path

from .views import LocationListAPIView, LocationLoadDataAPIView, RegionLoadDataAPIView, CityLoadDataAPIView


urlpatterns = [
    path("all/", LocationListAPIView.as_view(), name='locations_all'),
    path("load-data/", LocationLoadDataAPIView.as_view(), name='locations_load_data'),
    path("cities/load-data/", CityLoadDataAPIView.as_view(), name='locations_load_data_cities'),
    path("regions/load-data/", RegionLoadDataAPIView.as_view(), name='locations_load_data_regions'),

]
