from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .constants import LENGTH_COMMENT_FIELD, MAX_LENGTH_FIELD
from blog.managers import PostManager, PostQuerySet

User = get_user_model()


class DefaultPostSettingsModel(models.Model):
    """Универсальная абстрактная модель для модели постов."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(DefaultPostSettingsModel):
    """Модель категории для постов."""

    title = models.CharField(
        max_length=MAX_LENGTH_FIELD,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta(DefaultPostSettingsModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(DefaultPostSettingsModel):
    """Модель местоположения для постов."""

    name = models.CharField(
        max_length=MAX_LENGTH_FIELD,
        verbose_name='Название места'
    )

    class Meta(DefaultPostSettingsModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(DefaultPostSettingsModel):
    """Модель поста."""

    title = models.CharField(
        max_length=MAX_LENGTH_FIELD,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='blog_images',
        blank=True)

    objects = PostQuerySet.as_manager()
    postobj = PostManager()

    class Meta(DefaultPostSettingsModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для детального просмотра поста."""
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(DefaultPostSettingsModel):
    """Модель комментария к посту."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост',
    )
    text = models.TextField(verbose_name='Текст коментария')

    class Meta(DefaultPostSettingsModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        """Возвращает обрезанный текст комментария для отображения."""
        return self.text[:LENGTH_COMMENT_FIELD]
