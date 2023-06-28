from django.urls import path, include

from .views import AccountViewSet, BlockUserAPIView
from .routers import AccountRouter


router = AccountRouter()
router.register("accounts", AccountViewSet, "accounts")


urlpatterns = [
    path("", include(router.urls)),
    path("block/", BlockUserAPIView.as_view(), name="block_user"),

]
