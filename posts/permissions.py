from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Разрешение для проверки, является ли пользователь автором поста или администратором.
    Пользователь может редактировать/удалять только свои посты.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь администратором или автором поста
        return request.user.is_staff or obj.author == request.user