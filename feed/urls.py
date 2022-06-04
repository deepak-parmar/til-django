from django.urls import path
from .views import IndexView, PostCreateView, PostDetailView

app_name = "feed"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", PostDetailView.as_view(), name="view"),
    path("post/", PostCreateView.as_view(), name="post"),
]
