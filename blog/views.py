from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from meta.views import Meta  # type: ignore

from brdtheo.settings import IS_DEV_ENVIRONMENT

from .models import Post


def index(request: HttpRequest) -> HttpResponse:
    try:
        posts = Post.objects.all().filter(is_published=True).order_by("-created_at")
    except Post.DoesNotExist:
        raise Http404

    meta = Meta(
        title="Théo Billardey - Blog",
        description="Browse latest Théo Billardey's blog posts",
        url="/blog/",
        image="https://d3np79dr82q4gx.cloudfront.net/home/avatar.webp",
        use_title_tag=True,
        use_og=True,
        extra_custom_props=[
            ("http-equiv", "Content-Type", "text/html; charset=UTF-8"),
            ("name", "robots", "noindex") if IS_DEV_ENVIRONMENT else ("", "", ""),
        ],
    )

    return render(request, "index.html", context={"meta": meta, "posts": posts})


def post(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404

    meta = Meta(
        title=f"{post.title} - Théo Billardey",
        description=post.get_content_preview(),
        url=f"/blog/{post.slug}",
        image=post.thumbnail.url,
        use_title_tag=True,
        use_og=True,
        extra_custom_props=[
            ("http-equiv", "Content-Type", "text/html; charset=UTF-8"),
            ("name", "robots", "noindex") if IS_DEV_ENVIRONMENT else ("", "", ""),
        ],
    )

    return render(
        request,
        "post.html",
        context={
            "meta": meta,
            "thumbnail": post.thumbnail.url,
            "title": post.title,
            "content": post.get_content_html(),
            "categories": post.categories.all(),
            "created_at": post.created_at,
        },
    )
