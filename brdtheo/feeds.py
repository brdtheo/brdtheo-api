from datetime import datetime

from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from blog.models import Post


class RssPostFeeds(Feed):
    title = "Théo Billardey - Blog"
    link = "/blog/"
    description = "Latest blog posts from brdtheo.com."

    def items(self) -> QuerySet[Post, Post]:
        return Post.objects.filter(is_published=True).order_by("-created_at")[:10]

    def item_title(self, item: Post) -> str:
        return item.title

    def item_description(self, item: Post) -> str:
        return truncatewords(item.content, 100)

    def item_lastupdated(self, item: Post) -> datetime | None:
        return item.updated_at

    def item_link(self, item: Post) -> str:
        return reverse("blog-post", args=[item.slug])
