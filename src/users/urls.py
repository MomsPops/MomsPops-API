from django.urls import path, include

from .views import AccountViewSet, user_activation_api_view
from .routers import AccountRouter


router = AccountRouter()
router.register("accounts", AccountViewSet, "accounts")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/activate/<str:uid>/<str:token>/", user_activation_api_view, name="activate_user"),

]
