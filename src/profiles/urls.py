from django.urls import path, include

from .routers import ProfileRouter
from .views import ProfileViewSet


router = ProfileRouter()
router.register("", ProfileViewSet, "profiles")


urlpatterns = [
    path("", include(router.urls)),

]
