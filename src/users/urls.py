from django.urls import path, include

from .views import AccountViewSet, BlockUserViewSet
from .routers import AccountRouter


router = AccountRouter()
router.register("accounts", AccountViewSet, "accounts")
router.register("black-list", BlockUserViewSet, "black_list")


urlpatterns = [
    path("", include(router.urls)),

]
