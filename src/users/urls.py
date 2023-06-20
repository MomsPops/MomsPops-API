from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("users/", UserViewSet.as_view({"post": "create"}), name='users_create'),
    path("users/update", UserViewSet.as_view({"put": "update"}), name='users_update'),


]

