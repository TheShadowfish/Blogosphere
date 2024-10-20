from django.db import models

from django.db import models

from users.models import User


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите автора",
    )
    text = models.TextField(verbose_name="Текст", help_text="Введите текст")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", help_text="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования",
        help_text="Дата редактирования",
    )

    def __str__(self):
        return f"{self.text} - ({self.author.username})"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
