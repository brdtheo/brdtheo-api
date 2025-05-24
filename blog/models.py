from typing import Any, override

import markdown
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .enums import PostCategories


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


class PostThumbnail(models.Model):
    """A thumbnail image of a blog post"""

    url = models.URLField(
        help_text="The thumbnail media URL",
        db_comment="The thumbnail media URL",
    )
    created_at = models.DateTimeField(
        help_text="The creation date of the thumbnail object",
        db_comment="The creation date of the thumbnail object",
        default=timezone.now,
    )

    def __str__(self) -> str:
        return self.url


class Post(models.Model):
    """A representation of a blog post"""

    slug = models.SlugField(
        help_text="The URI encoded post title",
        db_comment="The URI encoded post title",
        unique=True,
        blank=True,
    )
    thumbnail = models.OneToOneField(PostThumbnail, on_delete=models.CASCADE)
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
        """Returns HTML code from rich text"""
        return markdown.markdown(
            self.content, extensions=["markdown.extensions.fenced_code"]
        )

    @override
    def save(self, *args: Any, **kwargs: Any) -> None:
        # Use None for initial updated_at value
        if self.pk:
            self.updated_at = timezone.now()

        # Automatically set slug
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
