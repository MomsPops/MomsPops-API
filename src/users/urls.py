from django.urls import path, include

from .views import AccountViewSet, BlackListViewSet, user_activation_api_view, FriendshipViewSet
from .routers import AccountRouter, BlackListRouter, FriendshipRouter

account_router = AccountRouter()
account_router.register("accounts", AccountViewSet, "accounts")

black_list_router = BlackListRouter()
black_list_router.register("black-list", BlackListViewSet, "black_list")

friendship_router = FriendshipRouter()
friendship_router.register("friendship", FriendshipViewSet, "friendship")


urlpatterns = [
    path("auth/activate/<str:uid>/<str:token>/", user_activation_api_view, name="activate_user"),
    path("", include(account_router.urls)),
    path("", include(black_list_router.urls)),
    path("", include(friendship_router.urls)),

]
