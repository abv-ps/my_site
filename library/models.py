"""
Models for the Library API.

This module defines the data models used in the Library API. It includes
the `Book` model for storing book information and the `TokenUsage` model
for tracking authentication token usage. It also provides a utility function
`hash_token` for hashing tokens.
"""

import hashlib

from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Model representing a book in the library.

    Attributes:
        title (CharField): The title of the book.
        author (CharField): The author of the book.
        genre (CharField): The genre of the book.
        publication_year (PositiveIntegerField): The year the book was published.
        user (ForeignKey): The user who added the book.
        created_at (DateTimeField): The date and time the book was created.
        updated_at (DateTimeField): The date and time the book was last updated.
        updated_by (CharField): The username of the user who last updated the book.
    """

    title: models.CharField = models.CharField(max_length=255)
    author: models.CharField = models.CharField(max_length=255)
    genre: models.CharField = models.CharField(max_length=100)
    publication_year: models.PositiveIntegerField = models.PositiveIntegerField()
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    updated_by: models.CharField = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns the title of the book as a string representation.

        Returns:
            str: The title of the book.
        """
        return str(self.title)


def hash_token(token: str) -> str:
    """
    Hashes a token using SHA256.

    Args:
        token (str): The token to hash.

    Returns:
        str: The hashed token.
    """
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


class TokenUsage(models.Model):
    """
    Model representing the usage of an authentication token.

    Attributes:
        user (ForeignKey): The user associated with the token.
        token_hash (CharField): The hashed token.
        created_at (DateTimeField): The date and time the token was used.
        ip_address (GenericIPAddressField): The IP address from which the token was used.
    """

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash: models.CharField = models.CharField(max_length=64, unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    ip_address: models.GenericIPAddressField = models.GenericIPAddressField(
        null=True, blank=True
    )

    def __str__(self) -> str:
        """
        Returns a string representation of the token usage.

        Returns:
            str: A string containing the username and hashed token.
        """
        return f"{self.user.username} - {self.token_hash}"

class AuthorBookAction(models.Model):
    ACTION_CHOICES = [
        ("author_created", "Author Created"),
        ("author_updated", "Author Updated"),
        ("book_created", "Book Created"),
        ("book_updated", "Book Updated"),
    ]

    author_id = models.IntegerField(null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True, blank=True)
    book_id = models.IntegerField(null=True, blank=True)
    book_title = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)