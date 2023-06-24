from django.urls import path

from .views import ReactionItemViewSet, ReactionViewSet

urlpatterns = [
    path("create/", ReactionViewSet.as_view({'get': 'list'}), name="reaction"),
    path('', ReactionItemViewSet.as_view({'get': 'list'}), name='create-list'),
    path('<int:pk>/', ReactionItemViewSet.as_view({'get': 'list'}), name='create-detail'),

]
