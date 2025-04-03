"""
Serializers for the Library API.

This module defines the serializers used in the Library API. It includes
serializers for the `Book` and `User` models, which handle the conversion
of model instances to and from JSON representations.
"""
from typing import Any

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer handles the conversion of Book model instances to and
    from JSON representations. It includes the username of the user who
    created the book as a read-only field.
    """

    user: serializers.ReadOnlyField = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        """
        Meta class for BookSerializer.

        Defines the model and fields to be serialized.
        """

        model: type[Book] = Book
        fields: str = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles the conversion of User model instances to and
    from JSON representations. It includes the password field for user
    creation, but it is write-only and not included in the serialized
    output.
    """

    password: serializers.CharField = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta class for UserSerializer.

        Defines the model and fields to be serialized.
        """

        model: User = User
        fields: tuple[str, ...] = ('username', 'password', 'email')

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Creates a new user instance.

        Hashes the password before saving the user.

        Args:
            validated_data (dict): Validated data from the serializer.

        Returns:
            User: The created user instance.
        """

        user: User = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
