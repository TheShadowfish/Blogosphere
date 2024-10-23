from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe


from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

    list_display = ("title", "text", "author_link", "created_at", "updated_at",)
    # фильтр по дате создания
    list_filter = ("created_at",)
    # поиск по названию поста
    search_fields = ("title",)
    # # ссылка на автора поста
    # list_display_links = ("title", "author",)

    @admin.display(description="ссылка на автора")
    def author_link(self, obj):

        # http://127.0.0.1:8000/admin/suppliers/supplier/3/change/

        if obj.author_id:
            my_reverse = reverse("admin:users_user_change", args=(obj.author_id,))
            return mark_safe(f'<a href="{my_reverse}">{obj.author}</a>')
        else:
            return None

    # @admin.display(description="комментарии")
    # def comments_link(self, obj):
    #     if obj.comment:
    #         longstring = ""
    #
    #         for c in obj.comment:
    #             c_id = c.id
    #             my_reverse = reverse("admin:comments_comment_change", args=(c_id))
    #             longstring += (f'<a href="{my_reverse}">{c.text}</a> ')
    #         return mark_safe(longstring)
    #
    #
    #     else:
    #         return None
