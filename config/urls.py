from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API приложение для написания и комментирования постов",
        default_version="v1.01",
        description="Приложение, позволяющее реализовать регистрацию пользователей, написание ими постов и написание "
                    "комментариев к ним",
        contact=openapi.Contact(email="shadowfish@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),
    path("posts/", include("posts.urls"), name="posts"),
    path("comments/", include("comments.urls"), name="comments"),

    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
