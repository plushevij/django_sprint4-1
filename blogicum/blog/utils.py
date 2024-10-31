from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

from .constants import POSTS_PER_PAGE


def paginate_query(request, queryset, per_page=POSTS_PER_PAGE):
    """Возвращает пагинированные данные для переданного запроса."""
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))


def check_author(request, model, id):
    instance = get_object_or_404(model, id=id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id=id)
    return True
