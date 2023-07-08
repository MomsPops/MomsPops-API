from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path('docs/', include(docs_urlpatterns)),   # docs urls

    path('auth/', include(
        [
            path('token/', TokenObtainPairView.as_view(), name="token_obtain"),
            path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
        ]
    )),

    # including other apps
    path("coordinates/", include("coordinates.urls")),
    path("locations/", include("locations.urls")),
    path("reactions/", include("reactions.urls")),
    path("notifications/", include("notifications.urls")),

    # `include()` through root url means that we are to register several viewsets at the same application,
    # but make their urls not relative ones
    path("", include("profiles.urls")),
    path("", include("users.urls")),

]
