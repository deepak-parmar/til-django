from django.views.generic import DetailView
from django.contrib.auth.models import User
from feed.models import Post

class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profile.html"
    model = User
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_post_count"] = Post.objects.all().filter(author=self.get_object()).count()
        # context["total_follower_count"] = Follower.objects.all().filter(author=self.get_object()).count()
        return context
    