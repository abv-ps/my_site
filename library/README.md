# Library API Module

This module provides a RESTful API for managing a library of books.
It includes endpoints for:

- Book CRUD operations (Create, Read, Update, Delete)
- User registration and authentication
- Token-based authentication (Rest)
- Book filtering and searching
- Pagination of book lists
- Administrative access for book deletion
- API documentation (Swagger/ReDoc)
- Token management for administrators

## Models:

- Book: Represents a book in the library.
- TokenUsage: Tracks usage of authentication tokens.

## Serializers:

- BookSerializer: Handles serialization and deserialization of Book objects.

## Views:

- BookViewSet: Provides CRUD operations for books.
- RegisterView: Handles user registration.
- CustomTokenObtainPairView: Handles user login and token generation.
- TokenRefreshView: Handles token refresh.
- DeleteBookView: Handles book deletion (admin only).
- DeleteUserView: Handles user deletion (admin only).
- AdminTokenView: Handles administrative token management.

## URLs:

- /api/: Includes all book-related endpoints.
- /api/register/: User registration.
- /api/token/: Token generation.
- /api/token/refresh/: Token refresh.
- /api/docs/: Swagger API documentation.
- /api/redoc/: ReDoc API documentation.
- /api/books/<int:pk>/delete/: Book deletion.
- /api/users/<int:pk>/delete/: User deletion.
- /api/admin/tokens/: Administrative token management.

## Dependencies:

- Django REST Framework
- Django REST Framework Simple JWT
- drf-yasg (Swagger/ReDoc)
- django-filter

This module follows PEP 8 style guidelines and includes type hints for improved code readability and maintainability.