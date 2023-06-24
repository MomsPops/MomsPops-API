from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path('docs/', include(docs_urlpatterns)),
    path('auth/', include(
        [
            path("", include("users.urls")),
            path('token/', TokenObtainPairView.as_view(), name="token_obtain"),
            path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
        ]
    )),
    path("coordinates/", include("coordinates.urls")),
    path("locations/", include("locations.urls")),
    path("profiles/", include("profiles.urls")),

]
