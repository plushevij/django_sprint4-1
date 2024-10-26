from django.forms import DateTimeInput, ModelForm, Textarea
from django.utils.timezone import localtime, now

from .constants import WINDOW_COMMENT_SIZE
from blog.models import Comment, Post, User


class PostForm(ModelForm):
    """Форма для создания и редактирования поста."""

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму,
        задавая начальное значение для даты публикации.
        """
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = localtime(
            now()).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        widgets = {
            'pub_date': DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(ModelForm):
    """Форма для добавления комментария к посту."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': Textarea({'rows': WINDOW_COMMENT_SIZE})}


class UserForm(ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
