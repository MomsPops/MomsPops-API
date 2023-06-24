from django.urls import path

from .views import ProfileViewSet


urlpatterns = [
    path("<str:username>/", ProfileViewSet.as_view({"get": "retrieve"}), name="profiles_detail"),
    path("<str:username>/update", ProfileViewSet.as_view({"patch": "update"}), name="profiles_update"),
    path("", ProfileViewSet.as_view({"get": "list"}), name="profiles_all"),

]
