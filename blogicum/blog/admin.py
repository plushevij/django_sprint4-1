from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.decorators import register
from django.contrib.auth.models import Group

from blog.models import Category, Comment, Location, Post


@register(Location)
class LocationAdmin(ModelAdmin):
    """Административная панель для модели Location."""

    list_display = ('name', 'is_published', 'created_at',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('name', 'is_published', 'created_at',)
    list_display_links = ('name',)


@register(Post)
class PostAdmin(ModelAdmin):
    """Административная панель для модели Post."""

    list_display = (
        'title',
        'author',
        'category',
        'location',
        'is_published',
        'created_at'
    )
    list_editable = ('is_published', 'location', 'category',)
    search_fields = ('title', 'text', )
    list_filter = ('category', 'is_published', 'location', 'author',)
    list_display_links = ('title',)


@register(Category)
class CategoryAdmin(ModelAdmin):
    """Административная панель для модели Category."""

    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'slug',)
    list_filter = ('title', 'is_published', 'created_at',)
    list_display_links = ('title', 'slug')


@register(Comment)
class CommentAdmin(ModelAdmin):
    """Административная панель для модели Comment."""

    list_display = (
        'text',
        'post',
        'author',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('text',)
    list_filter = ('post', 'is_published', 'created_at',)


site.empty_value_display = '-- Не задано --'
site.unregister(Group)
