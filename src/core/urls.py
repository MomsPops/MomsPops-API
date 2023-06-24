from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("coordinates/", include("coordinates.urls")),
    path("locations/", include("locations.urls")),
    path("reactions/", include("reactions.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
