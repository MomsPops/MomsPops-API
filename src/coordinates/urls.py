from django.urls import path

from .views import CoordinateNearAPIView, CoordinateViewSet, CoordinateDecodeAPIView


urlpatterns = [
    path("set/", CoordinateViewSet.as_view({"post": "create"}), name='coordinates_create'),
    path("delete/", CoordinateViewSet.as_view({"delete": "destroy"}), name="coordinates_destroy"),
    path("users-near/", CoordinateNearAPIView.as_view(), name="coordinates_near"),
    path("decode/", CoordinateDecodeAPIView.as_view(), name="coordinates_decode"),

]
