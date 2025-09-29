from rest_framework.serializers import ModelSerializer

from .models import Post, PostCategory


class PostCategorySerializer(ModelSerializer):
    class Meta: # type: ignore
        model = PostCategory
        fields = "__all__"


class PostSerializer(ModelSerializer):
    class Meta: # type: ignore
        model = Post
        fields = "__all__"
