from django.views.generic import ListView
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
    queryset = []

    # Format every date
    for post in Post.objects.all().order_by("dateCreated"):
        # check if post is modified
        if post.dateCreated == post.dateModified:
            post.dateModified = False
        else:
            post.dateModified = formatDate(post.dateModified)
        post.dateCreated = formatDate(post.dateCreated)
        queryset.append(post)
