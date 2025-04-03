"""
Signal handlers for the Library API.

This module defines signal handlers for the Library API. It includes a
signal handler that updates the `updated_by` field of `Book` instances
when a `User` instance is deleted.
"""
from typing import Any

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Book


@receiver(post_delete, sender=User)
def update_books_on_user_delete(sender: User, instance: User, **kwargs: dict[str, Any]) -> None:
    """
    Signal handler that updates the 'updated_by' field of Book instances when a User is deleted.

    When a User instance is deleted, this signal handler updates all Book instances
    where the 'updated_by' field matches the deleted user's username. It appends
    "(видалено)" to the username to indicate that the user has been deleted.

    Args:
        sender (User): The model class that sent the signal.
        instance (User): The actual instance being deleted.
        **kwargs (dict): Additional keyword arguments passed by the signal.
    """
    Book.objects.filter(updated_by=instance.username).update(
        updated_by=f"{instance.username} (видалено)"
    )
