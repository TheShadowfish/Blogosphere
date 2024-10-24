from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts.models import Post
from posts.serializers import PostSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(
        many=True, read_only=True, help_text="Пост комментария"
    )

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "post", "created_at", "updated_at", ]
        read_only_fields = [

            "author",
            "created_at",
            "post"
        ]

    def create(self, validated_data):
        """Привязка коментария к соответствующему посту, установка автором текущего пользователя"""

        post_id_raw = self.initial_data.get("post", None)

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        self.validated_data["author"] = user

        if post_id_raw:
            try:
                post = Post.objects.get(id=post_id_raw)
                self.context["post"] = post_id_raw
            except:
                raise ValidationError(f"Нет поста с таким ID {post_id_raw}")

        if self.is_valid():
            return Comment.objects.create(**self.validated_data)
