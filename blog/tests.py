import datetime

from django.db import IntegrityError
from django.test import TestCase

from .enums import PostCategories
from .models import Post, PostCategory, PostThumbnail


class PostTest(TestCase):
    def setUp(self):
        for category in PostCategories:
            PostCategory.objects.create(name=category)
        category_list = PostCategory.objects.all()
        thumbnail = PostThumbnail.objects.create(
            url="https://picsum.photos/seed/cv8JaiP/500/500"
        )
        post = Post.objects.create(
            title="Test Post",
            content="lorem ipsum dolor sit amet",
            thumbnail=thumbnail,
        )
        post.categories.set(category_list)
        self.post = post
        self.thumbnail = thumbnail

    def test_create(self):
        """Correctly creates a post"""
        assert type(self.post.slug) is str
        assert self.post.slug == "test-post"
        assert type(self.post.title) is str
        assert self.post.title == "Test Post"
        assert type(self.post.content) is str
        assert self.post.content == "lorem ipsum dolor sit amet"
        assert isinstance(self.post.created_at, datetime.date)
        assert self.post.updated_at is None
        assert type(self.post.get_content_html()) is str
        assert self.post.get_content_html() == "<p>lorem ipsum dolor sit amet</p>"
        assert type(self.post.thumbnail.url) is str
        assert self.post.thumbnail.url == self.thumbnail.url
        assert type(self.post.is_published) is bool
        assert self.post.is_published is False

    def test_update(self):
        """Correctly updates a post"""
        self.post.title = "Updated title"
        self.post.save()
        assert self.post.title == "Updated title"
        assert self.post.slug == "updated-title"
        assert self.post.updated_at is not None

    def test_delete(self):
        """Correctly deletes a post"""
        self.post.delete()
        assert Post.objects.count() == 0

    def test_delete_cascade(self):
        """Correctly deletes the related post if a thumbnail is deleted"""
        self.thumbnail.delete()
        assert PostThumbnail.objects.count() == 0
        assert Post.objects.count() == 0

    def test_fail_create_no_thumbnail(self):
        """Fails to create a blog post if no assigned thumbnail"""
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                title="Post without thumbnail",
                content="lorem ipsum dolor sit amet",
            )
