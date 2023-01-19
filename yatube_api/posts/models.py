from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
ADMINS_POST_LENGHT = 15


class Group(models.Model):
    """Получаем модель для Группы постов."""

    title = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=100,
        unique=True,
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """Возвращаем название группы."""
        return self.title


class Post(models.Model):
    """Получаем модель Поста."""

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст нового поста',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts_in_group',
        verbose_name='Сообщество',
        help_text='Группа, к которой будет относиться пост',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_of_posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
        help_text='Загрузите картинку, если желаете',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        """Возвращаем текст Поста."""
        return (
            self.text[:ADMINS_POST_LENGHT] + '...'
            if len(self.text) >= ADMINS_POST_LENGHT
            else self.text
        )


class Comment(models.Model):
    """Получаем модель для написания комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий автора',
        help_text='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий к посту',
        help_text='Пост комментария',
    )
    text = models.TextField(
        verbose_name='Текст коммментария',
        help_text='Текст комментария',
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращаем текст Комментария."""
        return (
            self.text[:ADMINS_POST_LENGHT] + '...'
            if len(self.text) >= ADMINS_POST_LENGHT
            else self.text
        )


class Follow(models.Model):
    """Получаем модель для осуществления подписки."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор в подписке',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'following',
                ],
                name='unique_follow',
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """Возвращаем читаемую связку Подписки."""
        return (
            f'{self.user} подписан на {self.following}'
        )
