from django.urls import path

from .views import ProfileViewSet


urlpatterns = [
    path("<str:username>/", ProfileViewSet.as_view({"get": "retrieve"}), name="profiles_detail"),

]
