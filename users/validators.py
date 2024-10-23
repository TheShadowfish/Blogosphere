from rest_framework.exceptions import ValidationError


def validate_email_domain(value):
    """Валидатор домена электронной почты при создании пользователя"""

    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = value.split("@")[-1]

    if domain not in allowed_domains:
        raise ValidationError(f"Разрешены следующие домены {', '.join(allowed_domains)}")



def validate_password(value):
    """Валидатор пароля - что он длиннее 8 символов и содержит хотя бы одну цифру """
    if len(value) < 8:
        raise ValidationError("Пароль должен быть длиннее 8 символов")

    digits = [s for s in value if s in '1234567890']

    if len(digits) < 1:
        raise ValidationError("Строка должна содержать хотя бы одну цифру")


def validate_phone(value):
    """Валидатор корректности введенного номера телефона"""

    # убираем тире и пробелы если пользователь их ввел
    value = value.replace(" ", "").replace("-", "")

    # прибавляем '+7' если пользователь не ввел
    if not value.startswith("+7"):
        value = "+7" + value

    # если в номере не только цифры
    if not value[1:].isdigit():
        raise ValidationError("Номер телефона должен содержать только цифры")

    # если номер слишком длинный +79876543210
    if len(value) != 12:
        raise ValidationError(
            "Номер телефона должен состоять из 11 цифр, код +7 не учитывается, и подставляется автоматически."
        )


    return value
