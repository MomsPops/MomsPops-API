from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import AccountViewSet

router = DefaultRouter()
router.register("accounts", AccountViewSet)


urlpatterns = [
    path("accounts/", AccountViewSet.as_view({"post": "create"}), name='accounts_create'),
    path("accounts/update/", AccountViewSet.as_view({"patch": "update"}), name="accounts_update"),
    path("accounts/me/", AccountViewSet.as_view({"get": "retrieve"}), name="accounts_me"),

]
