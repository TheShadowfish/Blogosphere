from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    # отображаемые поля
    list_display = ("title", "author", "created_at", "updated_at")
    # фильтр по дате создания
    list_filter = ("created_at",)
    # поиск по названию поста
    search_fields = ("title",)
    # ссылка на автора поста
    list_display_links = ("title", "author",)

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели, чтобы автоматически устанавливать автора как текущего пользователя.
        """
        if not obj.pk:  # Если это новый объект (пост)
            obj.author = request.user  # Устанавливаем текущего пользователя как автора
        super().save_model(request, obj, form, change)