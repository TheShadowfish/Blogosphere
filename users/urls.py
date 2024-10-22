from django.urls import path, include
from .apps import UsersConfig

from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

]



