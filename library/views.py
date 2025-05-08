"""
API Views for the Library Application.

This module defines the API views for the Library application. It includes
views for managing books, user registration, token handling, and administrative
token management.
"""
from typing import Optional, List, Dict, Any

from django.apps import apps
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.request import Request
from rest_framework.views import View
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Book, TokenUsage
from .serializers import BookSerializer, UserSerializer
from .token_manager import TokenManager


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access for all users
    and delete access for admin users only.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        """
        Checks if the user has permission to perform the requested action.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['publication_year', 'title']

    def perform_create(self, serializer: BookSerializer) -> None:
        """
        Saves the book with the current user as the creator.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer: BookSerializer) -> None:
        """
        Saves the book with the current user as the updater.
        """
        serializer.save(updated_by=self.request.user.username)


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, *args: List[Any], **kwargs: Dict[str, Any]) -> Response:
        """
        Creates a new user and generates tokens.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object containing tokens and status.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])

        ip_address = request.META.get('REMOTE_ADDR')
        token_key = TokenManager.generate_and_save_token(user, ip_address)

        response = Response({'token': token_key}, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie('token', token_key)
        return response


def delete_instance(model_name: str, pk: int) -> Response:
    """
    Generic function to delete an instance of a model.

    Args:
        model_name (str): The name of the model (e.g., 'myapp.User').
        pk (int): The primary key of the instance.

    Returns:
        Response: The API response.
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
    Generic view for deleting instances.
    """

    def destroy(self, request: Request, model_name: str, pk: int) -> Response:
        """
        Deletes an instance of a model.

        Args:
            request (Request): The request object.
            model_name (str): The name of the model.
            pk (int): The primary key of the instance.

        Returns:
            Response: The API response.
        """
        return delete_instance(model_name, int(pk))


class DeleteBookView(GenericDeleteView):
    """
    View for deleting a book.
    """
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request: Request, pk: int, model_name: str = "library_app.Book") -> Response:
        """
        Deletes a book instance.

        Args:
            request (Request): The request object.
            model_name (str): The name of the model (default "library_app.Book").
            pk (int): The primary key of the book instance.

        Returns:
            Response: The API response.
        """
        return super().delete(request, model_name, pk)


class DeleteUserView(GenericDeleteView):
    """
    View for deleting a user.
    """
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request: Request, model_name: str, pk: int) -> Response:
        """
        Deletes a user instance.

        Args:
            request (Request): The request object.
            model_name (str): The name of the model (always "auth.User").
            pk (int): The primary key of the user instance.

        Returns:
            Response: The API response.
        """
        return super().delete(request, "auth.User", pk)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pairs.
    """

    def post(self, request: Request, *args: List[Any], **kwargs: Dict[str, Any]) -> Response:
        """
        Generates and saves token usage on successful login.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object containing tokens.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            ip_address = request.META.get('REMOTE_ADDR')
            TokenManager.save_token_usage(user, response.data['access'], ip_address)
        return response


class AdminTokenView(generics.GenericAPIView):
    """
    View for managing admin tokens.
    """
    queryset = TokenUsage.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Lists token usage information.

        Allows administrators to retrieve a list of token usage records.
        Optionally, it can filter the records by user ID.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: A response containing the list of token usage records.
        """
        user_id: str = request.query_params.get("user_id")
        queryset = self.get_queryset().filter(user_id=user_id) \
            if user_id else self.get_queryset()

        data = [{
            'id': token.id,
            'user': token.user.username,
            'token_hash': token.token_hash,
            'created_at': token.created_at,
            'ip_address': token.ip_address
        } for token in queryset]
        return Response(data)

    def destroy(self, request: Request, *args: List[Any], **kwargs: Dict[str, Any]) -> Response:
        """
        Deletes a token usage instance.

        Allows administrators to delete a specific token usage record by its primary key.

        Args:
            request (Request): The request object.
            *args (List[Any]): Additional positional arguments (not used).
            **kwargs (Dict[str, Any]): Additional keyword arguments, including:
                - pk (Optional[str]): The primary key of the token usage instance.

        Returns:
            Response: A response indicating the success or failure of the deletion.
        """
        pk_str: Optional[str] = str(kwargs.get("pk"))

        if not pk_str or not pk_str.isdigit():
            return Response({"error": "Invalid token ID"}, status=status.HTTP_400_BAD_REQUEST)

        token = get_object_or_404(TokenUsage, pk=int(pk_str))
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
