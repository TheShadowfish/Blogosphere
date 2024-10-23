from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsOwnerOrAdmin


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка пользователей"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание нового пользователя")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление выбранного пользователя"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление выбранного пользователя"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление (частичное) выбранного пользователя"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о пользователе"),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки всех операций CRUD для модели User.

    CREATE: все пользователи (регистрация).
    READ: администратор/авторизованные пользователи.
    UPDATE: администратор/пользователь может редактировать только себя./
    DELETE: администратор.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["partial_update", "update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """Возвращает список разрешений для каждого действия."""

        permission_classes = {
            "create": [AllowAny],  # Разрешаем всем доступ к регистрации
            "retrieve": [
                IsAuthenticated,
                IsOwnerOrAdmin,
            ],  # Пользователь может читать себя, админ — всех
            "update": [
                IsAuthenticated,
                IsOwnerOrAdmin,
            ],  # Пользователь может редактировать себя, админ — всех
            "partial_update": [
                IsAuthenticated,
                IsOwnerOrAdmin,
            ],  # Пользователь может редактировать себя, админ — всех
            "destroy": [
                IsAdminUser
            ],  # Только администратор может удалять пользователей
            "list": [
                IsAdminUser,
            ],  # Только администратор может видеть список всех пользователей
        }.get(
            self.action, [IsAuthenticated, IsAdminUser]
        )  # По умолчанию только администратор и авторизованные пользователи

        return [permission() for permission in permission_classes]
