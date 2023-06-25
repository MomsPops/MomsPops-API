from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

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
]
