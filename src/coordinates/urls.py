from django.urls import path

# from .views import CoordinateNearAPIView, CoordinateViewSet, CoordinateDecodeAPIView
from .cache_views import set_coordinate, delete_coordinate, get_near_coordinates


urlpatterns = [
    # path("set/", CoordinateViewSet.as_view({"post": "create"}), name='coordinates_create'),
    # path("delete/", CoordinateViewSet.as_view({"delete": "destroy"}), name="coordinates_destroy"),
    # path("users-near/", CoordinateNearAPIView.as_view(), name="coordinates_near"),
    # path("decode/", CoordinateDecodeAPIView.as_view(), name="coordinates_decode"),

    # cache-based views
    path("set/", set_coordinate, name='set_coordinate'),
    path("delete/", delete_coordinate, name='delete_coordinate'),
    path("near/", get_near_coordinates, name='get_near_coordinates'),

]
