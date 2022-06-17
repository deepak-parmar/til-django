import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from follower.models import Follower


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


def formatPostDates(posts):
    formattedPost = []
    for post in posts:
        # check if post is modified
        if post.dateCreated == post.dateModified:
            post.dateModified = False
        else:
            post.dateModified = formatDate(post.dateModified)
        post.dateCreated = formatDate(post.dateCreated)
        formattedPost.append(post)
    return posts


class IndexView(TemplateView):
    http_method_names = ["get"]
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = []
        if self.request.user.is_authenticated:
            # List of users followed by current user
            following = list(
                Follower.objects.filter(followedBy=self.request.user).values_list(
                    "following", flat=True
                )
            )
            # Filter out posts that are from the following list
            posts = formatPostDates(
                Post.objects.filter(author__in=following).order_by("-dateCreated")
            )
        else:
            posts = formatPostDates(list(Post.objects.all().order_by("-dateCreated")))
        context["posts"] = posts
        return context


class PostExploreView(ListView):
    http_method_names = ["get"]
    template_name = "explore.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        self.queryset = formatPostDates(
            list(Post.objects.all().order_by("-dateCreated"))
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["explore_active"] = True
        return context


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
            post.dateModified = post.dateModified
        post.dateCreated = post.dateCreated
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

    # def form_valid(self, form):
    #     print("!!!!!!!!!!!!!!gets here")
    #     post = form.save(commit=False)
    #     # Fill author field with current user
    #     post.author = self.request.user
    #     post.save()
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        newPost = Post.objects.create(
            content=request.POST.get("content"), author=request.user
        )
        # if incoming request is ajax
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            newPost.dateCreated = formatDate(newPost.dateCreated)
            return render(
                request,
                "./components/card.html",
                {"post": newPost},
                content_type="application/html",
            )
        else:
            return HttpResponseRedirect(self.success_url)
