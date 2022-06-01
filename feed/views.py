from django.views.generic import ListView
from .models import Post


class IndexView(ListView):
    http_method_names = ["get"]
    model = Post
    context_object_name = "posts"
    # order posts by date
    queryset = Post.objects.all().order_by("date")
    template_name = "index.html"
