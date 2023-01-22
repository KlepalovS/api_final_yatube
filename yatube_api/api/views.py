from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnlyPermission
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_post(self):
        """Получаем пост для комментария."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получаем queryset."""
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$following__username',)

    def get_queryset(self):
        """Получаем queryset для конкретного юзера."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(user=self.request.user)
