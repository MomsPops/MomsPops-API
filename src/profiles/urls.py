from django.urls import path, include

from .routers import ProfileRouter, PostRouter
from .views import ProfileViewSet, PostViewSet


profile_router = ProfileRouter()
profile_router.register("profiles", ProfileViewSet, "profiles")

post_router = PostRouter()
post_router.register("posts", PostViewSet, "posts")


urlpatterns = [
    path("", include(profile_router.urls)),
    path("", include(post_router.urls)),

]
