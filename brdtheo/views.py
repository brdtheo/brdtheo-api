from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from blog.models import Post


def index(request: HttpRequest) -> HttpResponse:
    # Retrieve the latest blog post. If none, hide the section
    try:
        latest_post = Post.objects.latest("created_at")
    except Post.DoesNotExist:
        latest_post = None

    visited_country_list = [
        "france",
        "germany",
        "luxembourg",
        "spain",
        "austria",
        "japan",
    ]
    to_visit_country_list = [
        "thailand",
        "united_states",
        "china",
        "italy",
        "poland",
    ]

    return render(
        request,
        "brdtheo/index.html",
        context={
            "latest_post": latest_post,
            "visited_country_list": visited_country_list,
            "to_visit_country_list": to_visit_country_list,
        },
    )
