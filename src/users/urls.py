from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="users")


urlpatterns = [

]

urlpatterns += router.urls
