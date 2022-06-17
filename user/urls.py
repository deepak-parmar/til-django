from django.urls import path
from .views import ProfileDeleteView, ProfileDetailView, FollowView, ProfileNameUpdateView

app_name = "user"

urlpatterns = [
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
    path("<str:username>/follow/", FollowView.as_view(), name="follow"),
    path("delete/<str:username>/", ProfileDeleteView.as_view(), name="delete"),
    path("update-name/<str:username>/", ProfileNameUpdateView.as_view(), name="update-name"),
]
