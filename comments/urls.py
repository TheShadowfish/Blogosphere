from django.urls import path, include
from comments.apps import CommentsConfig

from rest_framework.routers import DefaultRouter
from .views import CommentViewSet


app_name = CommentsConfig.name

router = DefaultRouter()
router.register(r"", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]