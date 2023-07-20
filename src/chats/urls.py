from django.urls import path, include

from .views import GroupViewSet
from .routers import GroupRouter


router = GroupRouter()
router.register("groups", GroupViewSet, "groups")


urlpatterns = [
    path("", include(router.urls)),

]
