from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .models import Post, PostCategory
from .serializers import PostCategorySerializer, PostSerializer


class PostCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

    @action(detail=False, methods=["get"])
    def latest(self, request: HttpRequest) -> HttpResponse:
        latest_post = Post.objects.last()
        serializer = PostSerializer(latest_post)
        return Response(serializer.data, status=HTTP_200_OK)
