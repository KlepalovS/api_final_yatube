from django.core.exceptions import PermissionDenied

from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnlyPermission
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Follow, Group, Post


class CustomBaseViewSet(viewsets.ModelViewSet):
    """Кастомный базовый вьюсет с переназначенными методами update, destroy."""

    def perform_update(self, serializer):
        """Переопределяем метод update."""
        if self.get_object().author != self.request.user:
            raise PermissionDenied('Чужой контент изменять нельзя!')
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Переопределяем метод destroy."""
        if self.get_object().author != self.request.user:
            raise PermissionDenied('Чужой контент удалять нельзя!')
        return super(CustomBaseViewSet, self).destroy(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(CustomBaseViewSet):
    """Вьюсет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(author=self.request.user)


class CommentViewSet(CustomBaseViewSet):
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


class FollowViewSet(CustomBaseViewSet):
    """Вьюсет для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$following__username',)

    def get_queryset(self):
        """Получаем queryset для конкретного юзера."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(user=self.request.user)
