from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager


from users.validators import validate_email_domain, validate_password, validate_phone

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    username = models.CharField(max_length=40, unique=True, verbose_name="логин", help_text="Введите логин")

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите электронную почту, разрешены домены: mail.ru, yandex.ru",
        validators=[validate_email_domain],
    )
    password = models.CharField(
        verbose_name="Пароль",
        help_text="Введите пароль, должен быть не менее 8 символов, должен включать цифры",
        validators=[validate_password],
    )

    phone_number = models.CharField(max_length=17, verbose_name="телефон",
                                    help_text="Введите номер телефона в формате 999 123 45 67, +7 подставится "
                                              "автоматически",
                                    unique=True, null=True, validators=[validate_phone])
    birth_date = models.DateField(verbose_name="дата рождения", help_text="Введите вашу дату рождения", null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания",
                                  help_text="Введите дату создания пользователя")
    updated_at = models.DateField(auto_now=True, verbose_name="дата редактирования",
                                  help_text="Введите дату редактирования пользователя")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.username} - ({self.email})"

    def clean_phone(self):
        if self.phone_number is not None:
            # Убираем пробелы
            phone = self.phone_number.replace(" ", "").replace("-", "")
            # Добавляем код +7, если не введен
            if not phone.startswith("+7"):
                phone = "+7" + phone
            return phone

    def save(self, *args, **kwargs):
        # Перед сохранением форматируем номер телефона
        self.phone_number = self.clean_phone()
        super().save(*args, **kwargs)
