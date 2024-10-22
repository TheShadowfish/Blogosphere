from datetime import date

import re

from rest_framework.exceptions import ValidationError


def validate_post_title(value):
    """Проверка, что автор в заголовок не вписал запрещенные слова"""

    bad_words = ["ерунда", "глупость", "чепуха"]

    words = value.split()

    # for w in words:
    #     if w.lower() in bad_words:
    #         raise ValidationError(f"Запрещены названия постов, содержащие следующие слова: {', '.join(bad_words)}")

    for word in bad_words:
        if re.search(rf"\b{word}\b", value, re.IGNORECASE):
            raise ValidationError(f"Запрещены названия постов, содержащие следующие слова: {', '.join(bad_words)}")



def validate_author_age(author):
    """Проверка возраста автора (не менее 18 лет)"""
    if not author.birth_date:
        raise ValidationError("У автора должна быть указана дата рождения для публикации постов.")

    today = date.today()

    birth = author.birth_date
    # birth = datetime.strptime(author.birth_date, "%Y-%m-%d").date()

    age = (
            today.year
            - birth.year
            - ((today.month, today.day) < (birth.month, birth.day))
    )


    age = (
            today.year
            - birth.year
            - ((today.month, today.day) < (birth.month, author.birth_date.day))
    )

    if age < 18:
        raise ValidationError("Автор должен быть старше 18 лет для публикации постов.")
