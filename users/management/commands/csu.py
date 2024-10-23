from django.core.management import BaseCommand

from users.models import User


import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
dot_env = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dot_env)


class Command(BaseCommand):
    help = "Создание учётки админа"

    def handle(self, *args, **options):
        user = User.objects.create(
            username="admin2",
            email="admin2@mail.ru",
            birth_date="1984-03-09",
            phone_number="+79876543210",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(os.getenv("ADMIN_PASSWORD"))
        user.save()
