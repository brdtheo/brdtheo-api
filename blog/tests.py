import datetime

from django.db import IntegrityError
from django.test import TestCase

from .enums import PostCategories
from .models import Post, PostCategory

test_post_content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam at ex sapien. Sed in tellus non dolor dapibus tincidunt in eget nisl. Aenean eget nunc pulvinar, accumsan quam non, aliquam mauris augue."


class PostTest(TestCase):
    def setUp(self):
        for category in PostCategories:
            PostCategory.objects.create(name=category)
        category_list = PostCategory.objects.all()
        post = Post.objects.create(
            title="Test Post",
            content=test_post_content,
            thumbnail="https://picsum.photos/seed/cv8JaiP/500/500",
        )
        post.categories.set(category_list)
        self.post = post

    def test_create(self):
        """Correctly creates a post"""
        assert type(self.post.slug) is str
        assert self.post.slug == "test-post"
        assert type(self.post.title) is str
        assert self.post.title == "Test Post"
        assert type(self.post.content) is str
        assert self.post.content == test_post_content
        assert isinstance(self.post.created_at, datetime.date)
        assert self.post.updated_at is None
        assert type(self.post.get_content_html()) is str
        assert self.post.get_content_html() == f"<p>{test_post_content}</p>"
        assert type(self.post.get_content_preview()) is str
        assert len(self.post.get_content_preview()) == 150
        assert len(self.post.get_content_preview(180)) == 180
        assert type(self.post.thumbnail) is str
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

    def test_fail_create_no_thumbnail(self):
        """Fails to create a blog post if no assigned thumbnail"""
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                title="Post without thumbnail",
                content="lorem ipsum dolor sit amet",
            )
