from django.contrib import admin

from .models import Post, PostCategory, PostThumbnail


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    list_per_page = 10


@admin.register(PostThumbnail)
class PostThumbnailAdmin(admin.ModelAdmin):
    list_display = ("url", "created_at")
    list_per_page = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "thumbnail")
    list_per_page = 10
    list_filter = ("categories",)
    filter_horizontal = ("categories",)
    list_display_links = (
        "title",
        "slug",
    )
    search_fields = ("title",)
