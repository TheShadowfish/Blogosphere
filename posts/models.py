from django.db import models

from comments.models import Comment
from posts.validators import validate_post_title, validate_author_age
from users.models import User

NULLABLE = {"blank": True, "null": True}
# Create your models here.


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
        validators=[validate_post_title],
    )
    text = models.TextField(verbose_name="Текст", help_text="Введите текст")
    image = models.ImageField(
        verbose_name="Изображение",
        help_text="Загрузите изображение, если оно есть",
        upload_to="posts/",
        **NULLABLE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите автора",
        validators=[validate_author_age]
    )
    comment = models.ManyToManyField(
        Comment, verbose_name="Комментарии", help_text="Добавьте комментарии",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", help_text="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования",
        help_text="Дата редактирования",
    )

    def __str__(self):
        return f"{self.title} - ({self.author.username})"

    # Проверка возраста автора поста
    def clean(self):
        super().clean()
        validate_author_age(self.author)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"