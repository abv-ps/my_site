"""
Token management utilities for the Library API.

This module provides utility functions for generating and saving authentication tokens.
It includes the `TokenManager` class, which contains static methods for generating
JWT token pairs and saving token usage information.
"""
from typing import Optional

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import TokenUsage, hash_token


class TokenManager:
    """
    Utility class for managing authentication tokens.
    """

    @staticmethod
    def generate_tokens(user: User) -> dict[str, str]:
        """
        Generates JWT token pairs (refresh and access) for a user.

        Args:
            user (User): The user for whom to generate tokens.

        Returns:
            dict: A dictionary containing the refresh and access tokens.
        """
        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh.access_token)
        return {
            'refresh': str(refresh),
            'access': access_token,
        }

    @staticmethod
    def save_token_usage(user: User, access_token: str, ip_address: Optional[str] = None) -> None:
        """
        Saves the usage of an access token.

        Args:
            user (User): The user associated with the token.
            access_token (str): The access token.
            ip_address (str, optional): The IP address from which the token was used.
        """
        TokenUsage.objects.create(user=user,
                                  token_hash=hash_token(access_token),
                                  ip_address=ip_address
                                  )
