from typing import Any

import markdown
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from brdtheo.utils import strip_tags

from .enums import PostCategories
from .markdown_extensions import ImageSizesExtension


class PostCategory(models.Model):
    """A category assignable to multiple posts"""

    name = models.CharField(
        help_text="The category name",
        db_comment="The category name",
        max_length=20,
        unique=True,
        choices=PostCategories,  # type: ignore
    )
    created_at = models.DateTimeField(
        help_text="The creation date of the category object",
        db_comment="The creation date of the category object",
        default=timezone.now,
    )

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """A representation of a blog post"""

    slug = models.SlugField(
        help_text="The URI encoded post title",
        db_comment="The URI encoded post title",
        unique=True,
        blank=True,
        max_length=100,
    )
    thumbnail = models.URLField(
        help_text="The post thumbnail media URL",
        db_comment="The post thumbnail media URL",
    )
    categories = models.ManyToManyField(PostCategory)
    title = models.CharField(
        help_text="The post title, describing the global topic",
        db_comment="The post title, describing the global topic",
        max_length=60,
    )
    content = models.TextField(
        help_text="The post body/content, containing rich text for Markdown display",
        db_comment="The post body/content, containing rich text for Markdown display",
    )
    is_published = models.BooleanField(
        help_text="Defines if a post is published or hidden",
        db_comment="Defines if a post is published or hidden",
        default=False,
    )
    created_at = models.DateTimeField(
        help_text="The creation date of the post",
        db_comment="The creation date of the post",
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        help_text="The most recent update date of the post",
        db_comment="The most recent update date of the post",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    def get_content_html(self) -> str:
        """Returns HTML code from markdown"""
        return markdown.markdown(
            self.content,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.extra",
                ImageSizesExtension(),
            ],
        )

    def get_content_preview(self, max_length: int = 150) -> str:
        """Returns a portion of the post in text only"""
        stripped_content = strip_tags(self.get_content_html())
        return f"{stripped_content[: max_length - 3]}..."

    def save(self, *args: Any, **kwargs: Any) -> None:
        # Use None for initial updated_at value
        if self.pk:
            self.updated_at = timezone.now()

        # Automatically set slug if not defined or title is updated
        if not self.slug or (slugify(self.title) != self.slug):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
