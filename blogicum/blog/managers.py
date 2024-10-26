from django.db.models import Count, Manager, QuerySet
from django.utils.timezone import now


class PostQuerySet(QuerySet):
    """
    Кастомный QuerySet для модели Post,
    с передопределенными методами фильтрации и аннотаций.
    """

    def with_related_data(self):
        """
        Выбирает связанные объекты (автора, категорию и местоположение)
        для оптимизации запросов.
        """
        return self.select_related('author', 'category', 'location')

    def published(self):
        """
        Фильтрует посты, которые опубликованы
        и чья категория также опубликована.
        """
        return self.filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True
        )

    def comment_count(self):
        """
        Аннотирует количество комментариев к постам
        и сортирует их по дате публикации.
        """
        return self.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def by_author(self, author):
        """Возвращает посты конкретного автора."""
        return self.filter(author=author)

    def by_category(self, category):
        """Возвращает посты, принадлежащие конкретной категории."""
        return self.filter(category=category)


class PostManager(Manager):
    """
    Кастомный менеджер для модели Post
    с методами для работы с опубликованными постами.
    """

    def get_queryset(self):
        """Возвращает базовый QuerySet с связанными объектами."""
        return PostQuerySet(self.model).with_related_data()

    def get_pub(self):
        """Возвращает опубликованные посты."""
        return self.get_queryset().published()

    def get_for_index(self):
        """
        Возвращает посты для отображения на главной странице
        с количеством комментариев.
        """
        return self.get_pub().comment_count()

    def get_for_category(self, category):
        """
        Возвращает посты для конкретной категории
        с аннотацией количества комментариев.
        """
        return self.get_pub().by_category(category).comment_count()

    def get_for_profile(self, author):
        """
        Возвращает опубликованные посты конкретного автора
        с количеством комментариев.
        """
        return self.get_pub().by_author(author).comment_count()

    def get_for_profile_auth(self, author):
        """
        Возвращает все посты конкретного автора
        с количеством комментариев,включая неопубликованные.
        """
        return self.get_queryset().by_author(author).comment_count()
