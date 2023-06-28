from django.urls import path, include

from .routers import ProfileRouter
from .views import ProfileViewSet, PostViewSet


router = ProfileRouter()
router.register("posts", PostViewSet, "posts")
router.register("profiles", ProfileViewSet, "profiles")


urlpatterns = [
    path("", include(router.urls)),

]
