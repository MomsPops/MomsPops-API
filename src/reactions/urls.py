from django.urls import path

from .views import ReactionItemViewSet, ReactionViewSet

urlpatterns = [
    path("", ReactionViewSet.as_view({'post': 'create', 'delete': 'destroy',
                                      "put": "update"}), name="reaction"),
    path('create/', ReactionItemViewSet.as_view({'get': 'list'}), name='reaction_create'),
    path('create/<int:pk>/', ReactionItemViewSet.as_view({'get': 'retrieve', 'post': "create", "put": "update",
                                                          "delete": "destroy"}), name='create_retrieve'),]
