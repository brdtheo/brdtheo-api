from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
)

from .models import Post, PostCategory


class PostCategorySerializer(ModelSerializer):
    class Meta:  # type: ignore
        model = PostCategory
        fields = "__all__"


class PostSerializer(ModelSerializer):
    preview = SerializerMethodField()
    url = HyperlinkedIdentityField(view_name="post-detail", lookup_field="slug")

    class Meta:  # type: ignore
        model = Post
        fields = "__all__"
        lookup_field = "slug"

    def get_preview(self, obj: Post) -> str:
        return obj.get_content_preview()
