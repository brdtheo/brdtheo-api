from rest_framework import viewsets

from .models import Post, PostCategory
from .serializers import PostCategorySerializer, PostSerializer


class PostCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
