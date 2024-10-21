from django.urls import path, include
from .apps import PostsConfig

from rest_framework.routers import DefaultRouter
from .views import PostViewSet


app_name = PostsConfig.name

router = DefaultRouter()
router.register(r"", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]