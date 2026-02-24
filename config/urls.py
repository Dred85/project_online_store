from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_prometheus import exports

urlpatterns = [
    path("admin/", admin.site.urls),
    path("metrics/", exports.ExportToDjangoView),
    path("", include("catalog.urls", namespace="catalog")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
