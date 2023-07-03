from django.urls import path

from .views import LocationListAPIView, LocationLoadDataAPIView, RegionLoadDataAPIView, CityLoadDataAPIView
from .views import load_regions_view, load_cities_view, load_locations_view


urlpatterns = [
    path("all/", LocationListAPIView.as_view(), name='locations_all'),
    path("load-data/", LocationLoadDataAPIView.as_view(), name='locations_load_data'),
    path("cities/load-data/", CityLoadDataAPIView.as_view(), name='locations_load_data_cities'),
    path("regions/load-data/", RegionLoadDataAPIView.as_view(), name='locations_load_data_regions'),

    # celery task views
    path("load-data-async/", load_locations_view, name='locations_load_data_async'),
    path("cities/load-data-async/", load_cities_view, name='locations_load_data_cities_async'),
    path("regions/load-data-async/", load_regions_view, name='locations_load_data_regions_async'),

]
