from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)
from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include(docs_urlpatterns)),
    path('auth/', include(
        [
            path("", include("users.urls")),
            path('token/', TokenObtainPairView.as_view(), name="token_obtain"),
            path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
        ]
    )),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
