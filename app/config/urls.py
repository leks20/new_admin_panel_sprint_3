from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("movies.api.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
