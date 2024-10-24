from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ["id", "text", "author_link", "created_at", "updated_at"]

    # list_display_links = ["id", "text"]

    @admin.display(description="ссылка на автора")
    def author_link(self, obj):

        # http://127.0.0.1:8000/admin/suppliers/supplier/3/change/

        if obj.author_id:
            my_reverse = reverse("admin:users_user_change", args=(obj.author_id,))
            return mark_safe(f'<a href="{my_reverse}">{obj.author}</a>')
        else:
            return None
