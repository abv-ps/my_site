from django.apps import apps
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Book, TokenUsage
from .serializers import BookSerializer, UserSerializer
from .token_manager import TokenManager


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to delete books.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['publication_year', 'title']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        tokens = TokenManager.generate_tokens(user)
        ip_address = request.META.get('REMOTE_ADDR')
        TokenManager.save_token_usage(user, tokens['access'], ip_address)
        return Response(tokens, status=status.HTTP_201_CREATED, headers=headers)


def delete_instance(model_name, pk):
    """
    Універсальна функція для видалення інстансу моделі.

    Args:
        model_name (str): Назва моделі (наприклад, 'myapp.User').
        pk (int): Первинний ключ інстансу.

    Returns:
        Response: Відповідь API.
    """
    try:
        model = apps.get_model(model_name)
    except LookupError:
        return Response(
            {"error": f"Model '{model_name}' not found."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    instance = get_object_or_404(model, pk=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GenericDeleteView(generics.GenericAPIView):
    """
    Універсальне представлення для видалення інстансів.
    """

    def delete(self, request, model_name, pk):
        return delete_instance(model_name, pk)


class DeleteBookView(GenericDeleteView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, model_name, pk):
        return super().delete(request, "library_app.Book", pk)


class DeleteUserView(GenericDeleteView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, model_name, pk):
        return super().delete(request, "auth.User", pk)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            ip_address = request.META.get('REMOTE_ADDR')
            TokenManager.save_token_usage(user, response.data['access'], ip_address)
        return response


class AdminTokenView(generics.ListAPIView, generics.DestroyAPIView):
    queryset = TokenUsage.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, user_id=None):
        if user_id:
            queryset = self.queryset.filter(user_id=user_id)
        else:
            queryset = self.queryset
        data = [{
            'id': token.id,
            'user': token.user.username,
            'token_hash': token.token_hash,
            'created_at': token.created_at,
            'ip_address': token.ip_address
        } for token in queryset]
        return Response(data)

    def destroy(self, request, pk):
        try:
            token = TokenUsage.objects.get(pk=pk)
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenUsage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
