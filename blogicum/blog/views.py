from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post, User
from .utils import paginate_query, check_author


def index(request):
    """Отображает главную страницу с пагинированными постами."""
    page_obj = paginate_query(request, Post.postobj.get_for_index())
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    """
    Отображает страницу с подробной информацией о посте
    и комментариями к нему.
    """
    post = get_object_or_404(Post.postobj.all(), id=post_id)
    if not post.author == request.user:
        post = get_object_or_404(Post.postobj.get_pub(), id=post_id)
    comments = post.comments.select_related('author')
    context = {'post': post, 'comments': comments, 'form': CommentForm()}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Отображает посты для конкретной категории."""
    cat = get_object_or_404(Category, slug=category_slug, is_published=True)
    page_obj = paginate_query(request, Post.postobj.get_for_category(cat))
    context = {'category': cat, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


@login_required
def create_post(request):
    """Создает новый пост. Доступна только авторизованным пользователям."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


def edit_post(request, post_id):
    """
    Редактирует существующий пост.
    Пользователь должен быть автором поста.
    """
    instance = get_object_or_404(Post, id=post_id)
    if check_author(request, Post, id=post_id) is None:
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=instance)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
        return render(request, 'blog/create.html', {'form': form})
    return redirect('blog:post_detail', post_id)


def delete_post(request, post_id):
    """Удаляет пост. Пользователь должен быть автором поста."""
    instance = get_object_or_404(Post, id=post_id)
    if check_author(request, Post, id=post_id) is None:
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=instance)
        if request.method == 'POST':
            instance.delete()
            return redirect('blog:profile', username=request.user.username)
        return render(request, 'blog/create.html', {'form': form})
    return redirect('blog:post_detail', post_id)


def profile(request, username):
    """Отображает профиль пользователя с его постами."""
    user = get_object_or_404(User, username=username)
    if not user == request.user:
        posts = Post.postobj.get_for_profile(user)
    else:
        posts = Post.postobj.get_for_profile_auth(user)
    context = {'profile': user, 'page_obj': paginate_query(request, posts)}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """
    Редактирует профиль пользователя.
    Доступно только авторизованным пользователям.
    """
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, post_id):
    """
    Добавляет новый комментарий к посту.
    Доступно только авторизованным пользователям.
    """
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """
    Редактирует существующий комментарий.
    Пользователь должен быть автором комментария.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if check_author(request, Comment, id=comment_id) is None:
        form = CommentForm(request.POST or None, instance=comment)
        context = {'form': form, 'comment': comment}
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
        return render(request, 'blog/comment.html', context)
    return redirect('blog:post_detail', post_id)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаляет комментарий. Пользователь должен быть автором комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if check_author(request, Comment, id=comment_id) is None:
        if request.method == 'POST':
            comment.delete()
            return redirect('blog:post_detail', post_id)
        return render(request, 'blog/comment.html', {'comment': comment})
    return redirect('blog:post_detail', post_id)
