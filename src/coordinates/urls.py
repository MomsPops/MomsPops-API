from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CoordinatesViewSet


router = DefaultRouter()
router.register("", CoordinatesViewSet)


urlpatterns = [
    path("set/", CoordinatesViewSet.as_view({"post": "create"}), name='coordinates_set'),
    path("users-near/", CoordinatesViewSet.as_view({"get": "all_near"}), name="coordinates_all_near"),

]
