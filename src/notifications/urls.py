from django.urls import path

from .views import PersonalNotificationViewSet


urlpatterns = [
    path("", PersonalNotificationViewSet.as_view({'get': 'list'}), name='get_notifications'),
    path("<int:pk>/", PersonalNotificationViewSet.as_view({'get': 'retrieve'}), name='get_notification'),
    path("<int:pk>/viewed/", PersonalNotificationViewSet.as_view({'post': 'viewed'}), name='change_notification'),
]
