from rest_framework import serializers
from .models import Post
import re
from datetime import date, datetime
from django.core.exceptions import ValidationError


# Валидатор возраста (не менее 18 лет)
def validate_author_age(author):
    if not author.birth_date:
        raise ValidationError("У автора должна быть указана дата рождения.")

    today = date.today()
    birth = datetime.strptime(author.birth_date, "%Y-%m-%d").date()

    age = (today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day)))

    if age < 18:
        raise ValidationError("Автор должен быть старше 18 лет для публикации постов.")


# Валидатор для запрещенных слов в заголовке поста
def validate_post_title(value):
    forbidden_words = ["ерунда", "глупость", "чепуха"]

    for word in forbidden_words:
        if re.search(rf"\b{word}\b", value, re.IGNORECASE):
            raise ValidationError(
                f"Заголовок не должен содержать запрещенные слова: {', '.join(forbidden_words)}."
            )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # depth = 1
        fields = ["id", "title", "text", "comment", "image", "author", "created_at", "updated_at", ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate(self, data):
        title = data.get("title")
        author = self.context["request"].user
        # Валидация возраста автора
        validate_author_age(author)
        # Валидация заголовка поста
        validate_post_title(title)
        return data
