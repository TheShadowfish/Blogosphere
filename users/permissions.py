from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешение, которое позволяет пользователям редактировать только свои данные, а администраторам — всех.
    """

    def has_object_permission(self, request, view, obj):
        # Только владелец или администратор может обновлять или удалять
        return request.user.is_staff or request.user.is_superuser or obj == request.user