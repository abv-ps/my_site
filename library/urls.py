"""
API URL Configuration.

This module defines the URL patterns for the Library API.
It includes routes for book management, user registration, token handling,
API documentation, and administrative token management.
"""

from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    BookViewSet,
    RegisterView,
    DeleteBookView,
    DeleteUserView,
    CustomTokenObtainPairView,
    AdminTokenView,
)

app_name: str = "api"

router: DefaultRouter = DefaultRouter()
router.register(r"books", BookViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="v1",
        description="API for managing books in a library",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("books/<int:pk>/delete/", DeleteBookView.as_view(), name="delete_book"),
    path("users/<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("admin/tokens/", AdminTokenView.as_view(), name="admin_tokens"),
    path("admin/tokens/<int:user_id>/", AdminTokenView.as_view(), name="admin_tokens_user"),
    path("admin/tokens/delete/<int:pk>/", AdminTokenView.as_view(), name="admin_tokens_delete"),
]
