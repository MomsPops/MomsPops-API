from django.urls import path

from .views import CoordinateNearAPIView, CoordinateCreateAPIView


urlpatterns = [
    path("set/", CoordinateCreateAPIView.as_view(), name='coordinates_set'),
    path("users-near/", CoordinateNearAPIView.as_view(), name="coordinates_near"),

]
