from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from meta.views import Meta  # type: ignore

from blog.models import Post
from brdtheo.settings import IS_DEV_ENVIRONMENT


class RobotsTxtView(TemplateView):
    template_name = "dev.robots.txt" if IS_DEV_ENVIRONMENT else "robots.txt"


def index(request: HttpRequest) -> HttpResponse:
    # Retrieve the latest blog post. If none, hide the section
    try:
        latest_post = Post.objects.filter(is_published=True).latest("created_at")
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

    meta = Meta(
        title="Théo Billardey",
        description="Welcome to my website. I am a Front-End engineer that loves traveling and car culture. Feel free to check out my work on GitHub or browse my blog posts.",
        url="/",
        image="https://d3np79dr82q4gx.cloudfront.net/home/avatar.webp",
        use_title_tag=True,
        use_og=True,
        extra_custom_props=[
            ("http-equiv", "Content-Type", "text/html; charset=UTF-8"),
            ("name", "robots", "noindex") if IS_DEV_ENVIRONMENT else ("", "", ""),
        ],
    )

    return render(
        request,
        "brdtheo/index.html",
        context={
            "meta": meta,
            "latest_post": latest_post,
            "visited_country_list": visited_country_list,
            "to_visit_country_list": to_visit_country_list,
        },
    )
