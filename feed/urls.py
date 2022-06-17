from django.urls import path
from .views import IndexView, PostCreateView, PostDetailView, PostExploreView

app_name = "feed"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("explore/", PostExploreView.as_view(), name="explore"),
    path("<int:pk>/", PostDetailView.as_view(), name="view"),
    path("post/", PostCreateView.as_view(), name="post"),
]
