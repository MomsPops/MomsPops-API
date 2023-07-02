from django.urls import path, include
from rest_framework import routers
from chats import views


router = routers.DefaultRouter()
router.register(r"groups", views.GroupViewSet)
router.register(r"chats", views.ChatViewSet)
router.register(r"messages", views.MessageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
