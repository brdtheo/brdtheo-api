from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet
from django.urls import reverse

from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self) -> QuerySet[Post, Post]:
        return Post.objects.filter(is_published=True).order_by("-created_at")

    def lastmod(self, item: Post) -> None | datetime:
        return item.updated_at


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self) -> list[str]:
        return [
            "home",
            "blog",
        ]

    def location(self, item: str) -> str:
        return reverse(item)


sitemaps = {"static": StaticViewSitemap, "posts": PostSitemap}
