from django.urls import path, include

from .views import AccountViewSet, BlackListViewSet, user_activation_api_view
from .routers import AccountRouter, BlackListRouter

account_router = AccountRouter()
account_router.register("accounts", AccountViewSet, "accounts")

black_list_router = BlackListRouter()
black_list_router.register("black-list", BlackListViewSet, "black_list")

urlpatterns = [
    path("auth/activate/<str:uid>/<str:token>/", user_activation_api_view, name="activate_user"),
    path("", include(account_router.urls)),
    path("", include(black_list_router.urls)),
  
]
