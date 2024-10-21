from rest_framework import serializers
from .models import User
from .validators import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        read_only=True, required=False
    )  # Поле password только для чтения, и это поле не обязательно

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "birth_date",
            "created_at",
            "updated_at",
            "password",
        ]

    def validate_password(self, value):
        """
        Вызываем валидатор для пароля, так как валидатор указанный в модели User через параметр validators не работает,
        Для API валидатор должен быть подключен через сериализатор
        """
        validate_password(value)
        return value


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True
    )  # Поле password только для записи, и это поле обязательно

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True, required=False
    )  # Поле password только для записи, и это поле не обязательно

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
