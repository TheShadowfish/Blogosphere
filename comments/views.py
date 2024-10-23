from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from .models import Comment
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.permissions import IsAuthorOrAdmin
from .serializers import CommentSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка комментариев"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание нового комментария")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление выбранного комментария"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление выбранного комментария"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление (частичное) выбранного комментария"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о комментарии"),
)
class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений для каждого действия.

        CREATE: авторизованные пользователи.
        READ: все пользователи.
        UPDATE: администратор/пользователь может редактировать только себя.
        DELETE: администратор/пользователь может удалять свои комментарии.
        """
        permission_classes = {
            "create": [
                IsAuthenticated
            ],  # Только авторизованные пользователи могут создавать посты
            "retrieve": [AllowAny],  # Все могут просматривать посты
            "update": [
                IsAuthenticated,
                IsAuthorOrAdmin,
            ],  # Пользователь может редактировать только свои посты, администратор — все
            "partial_update": [
                IsAuthenticated,
                IsAuthorOrAdmin,
            ],  # Пользователь может редактировать только свои посты, администратор — все
            "destroy": [
                IsAuthenticated,
                IsAuthorOrAdmin,
            ],  # Пользователь может удалять только свои посты, администратор — все.
            "list": [AllowAny],  # Все могут просматривать посты
        }.get(
            self.action, [IsAuthenticated, IsAuthorOrAdmin]
        )  # По умолчанию только авторизованные пользователи и автор поста или администратор

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как автора
        serializer.save(author=self.request.user)
