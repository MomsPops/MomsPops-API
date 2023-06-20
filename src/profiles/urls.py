from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, NoteViewSet


router = DefaultRouter()

router.register("profiles", ProfileViewSet, basename='profiles')
router.register("notes", NoteViewSet, basename='notes')


urlpatterns = [
    # path("profiles/", ProfileViewSet.as_view({"post": "create"}), name='profiles_create'),
    # path("profiles/", ProfileViewSet.as_view({"get": "list"}), name='profiles_list'),
    path("notes/<str:username>", NoteViewSet.as_view({"get": "list"}), name='notes_list')
]

urlpatterns += router.urls
