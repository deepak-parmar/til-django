from django.contrib import admin
from django.urls import include, path
from feed import urls as feed_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(feed_urls, namespace="feed")),
]
