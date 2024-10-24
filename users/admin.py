from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "birth_date",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")

    # фильтр по дате создания
    list_filter = ("created_at",)
    # поиск
    search_fields = ("username",)
    # ссылка
    list_display_links = ("username",)
