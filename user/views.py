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


class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):  # removed arg-kwargs to see what happens
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest(
                JsonResponse({"success": False, "message": "Missing parameters"})
            )

        try:
            requestedUser = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return HttpResponseBadRequest(
                JsonResponse({"success": False, "message": "User not found"})
            )

        if data["action"] == "follow":
            follower, created = Follower.objects.get_or_create(
                followedBy=request.user, following=requestedUser
            )
            print(follower, created)
        else:
            try:
                follower = Follower.objects.get(
                    followedBy=request.user, following=requestedUser
                )
            except Follower.DoesNotExist:
                follower = None

            # delete record of follower is found
            if follower:
                follower.delete()

            return JsonResponse(
                {
                    "success": True,
                    "button-label": "Unfollow"
                    if data["action"] == "follow"
                    else "Follow",
                }
            )


class ProfileDeleteView(DeleteView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = "/"