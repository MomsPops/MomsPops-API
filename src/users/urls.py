from django.urls import path, include

from .views import AccountViewSet
from .routers import AccountRouter


router = AccountRouter()
router.register("accounts", AccountViewSet, "accounts")


urlpatterns = [
    path("", include(router.urls)),

]
