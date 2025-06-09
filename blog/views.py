from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Post


def index(request: HttpRequest) -> HttpResponse:
    try:
        posts = Post.objects.all().filter(is_published=True).order_by("-created_at")
    except Post.DoesNotExist:
        raise Http404

    return render(request, "index.html", context={"posts": posts})


def post(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404

    return render(
        request,
        "post.html",
        context={
            "thumbnail": post.thumbnail.url,
            "title": post.title,
            "content": post.get_content_html(),
            "categories": post.categories.all(),
            "created_at": post.created_at,
        },
    )
