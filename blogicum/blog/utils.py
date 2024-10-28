from django.core.paginator import Paginator

from .constants import POSTS_PER_PAGE


def paginate_query(request, queryset, per_page=POSTS_PER_PAGE):
    """Возвращает пагинированные данные для переданного запроса."""
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))
