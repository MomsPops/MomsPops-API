from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet

chat_router = DefaultRouter()
chat_router.register('', ChatViewSet, basename='chats')

urlpatterns = [
    path('', include(chat_router.urls))
]
