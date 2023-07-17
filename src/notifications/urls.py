from django.urls import include, path

from .views import NotificationAccountViewSet
from .routers import NotificationAccountRouter


router = NotificationAccountRouter()
router.register("", NotificationAccountViewSet, "notifications")


urlpatterns = [
    path("", include(router.urls)),

]
