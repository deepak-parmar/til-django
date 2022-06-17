from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from feed.models import Post
from follower.models import Follower
from feed.views import formatPostDates


class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profile.html"
    model = User
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requestingUser = self.get_object()
        context["total_post_count"] = (
            Post.objects.all().filter(author=requestingUser).count()
        )
        context["total_following_count"] = len(
            list(
                Follower.objects.filter(followedBy=requestingUser).values_list(
                    "following", flat=True
                )
            )
        )

        followers = list(
            Follower.objects.filter(following=requestingUser).values_list(
                "followedBy", flat=True
            )
        )
        context["total_follower_count"] = len(followers)

        if self.request.user.is_authenticated:
            # if profile is user's own
            if self.request.user.id == requestingUser.id:
                # then do not provide follow/unfollow button
                context["show_follow_button"] = False
            else:
                context["show_follow_button"] = True
                context["beingFollowed"] = Follower.objects.filter(
                    following=requestingUser, followedBy=self.request.user
                ).exists()

        context["posts"] = formatPostDates(
            list(
                Post.objects.filter(author=requestingUser).order_by("-dateCreated")
            )
        )

        context["profile_active"] = True

        return context
