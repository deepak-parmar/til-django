from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from feed import urls as feed_urls
from user import urls as user_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(feed_urls, namespace="feed")),
    path("user/", include(user_urls, namespace="user")),
    re_path("", include("allauth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
