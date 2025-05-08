"""
Token management utilities for the Library API.

This module provides utility functions for generating and saving authentication tokens.
It includes the `TokenManager` class, which contains static methods for generating
JWT token pairs and saving token usage information.
"""
from typing import Optional
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import TokenUsage, hash_token

class TokenManager:
    """
    Utility class for managing DRF (non-JWT) authentication tokens.
    """

    @staticmethod
    def generate_token(user: User) -> str:
        """
        Generates or retrieves a DRF Token for a user.

        Args:
            user (User): The user for whom to generate the token.

        Returns:
            str: The authentication token.
        """
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def save_token_usage(user: User, token_key: str, ip_address: Optional[str] = None) -> None:
        """
        Saves the usage of a token.

        Args:
            user (User): The user associated with the token.
            token_key (str): The token key.
            ip_address (str, optional): The IP address from which the token was used.
        """
        TokenUsage.objects.create(
            user=user,
            token_hash=hash_token(token_key),
            ip_address=ip_address
        )

    @staticmethod
    def generate_and_save_token(user: User, ip_address: Optional[str] = None) -> str:
        """
        Generates a DRF token and saves its usage info.

        Args:
            user (User): The user for whom to generate the token.
            ip_address (str, optional): IP from which the token is issued.

        Returns:
            str: The authentication token.
        """
        token_key = TokenManager.generate_token(user)
        TokenManager.save_token_usage(user, token_key, ip_address)
        return token_key
