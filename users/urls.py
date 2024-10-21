from django.urls import path, include
from .apps import UsersConfig

from rest_framework.routers import DefaultRouter
from .views import UserViewSet


app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]