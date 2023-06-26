from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
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

    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("coordinates/", include("coordinates.urls")),
    path("locations/", include("locations.urls")),
    path("profiles/", include("profiles.urls")),
]
