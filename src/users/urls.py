from django.urls import path, include

from .views import AccountViewSet, BlackListViewSet
from .routers import AccountRouter, BlackListRouter


account_router = AccountRouter()
account_router.register("accounts", AccountViewSet, "accounts")

black_list_router = BlackListRouter()
black_list_router.register("black-list", BlackListViewSet, "black_list")


urlpatterns = [
    path("", include(account_router.urls)),
    path("", include(black_list_router.urls)),

]
