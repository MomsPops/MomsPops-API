from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, NoteViewSet


router = DefaultRouter()

router.register("profiles", ProfileViewSet, basename='profiles')
router.register("notes", NoteViewSet, basename='notes')


urlpatterns = [

]

urlpatterns += router.urls
