from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


# ? Worked without importing date from datetime
def formatDate(date):
    # if post was created today
    if date.date() == date.today().date():
        return f"Today · {date.strftime('%I:%M %p')}"
    # if post was created yesterday
    elif date.strftime("%d%m%Y") == date.today().strftime(
        f"{date.today().day-1:02d}%m%Y"
    ):
        return f"Yesterday · {date.strftime('%I:%M %p')}"
    # if post was created within the current year
    elif date.year == date.today().year:
        return date.strftime("%B %d · %I:%M %p")
    else:
        # show full format
        return date.strftime("%B %d, %Y · %I:%M %p")


class IndexView(ListView):
    http_method_names = ["get"]
    template_name = "index.html"
    model = Post
    context_object_name = "posts"

    # overwrite queryset
    def get_queryset(self):
        self.queryset = []
        # format every date
        for post in Post.objects.all().order_by("dateCreated"):
            # check if post is modified
            if post.dateCreated == post.dateModified:
                post.dateModified = False
            else:
                post.dateModified = formatDate(post.dateModified)
            post.dateCreated = formatDate(post.dateCreated)
            self.queryset.append(post)
        return super().get_queryset()


class PostDetailView(DetailView):
    http_method_names = ["get"]
    model = Post
    context_object_name = "post"
    template_name = "view.html"

    # Format date of requested post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        if post.dateCreated == post.dateModified:
            post.dateModified = False
        else:
            post.dateModified = formatDate(post.dateModified)
        post.dateCreated = formatDate(post.dateCreated)
        context["post"] = post
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post.html"
    fields = ["content"]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        # Get current user
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        # Fill author field with current user
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
