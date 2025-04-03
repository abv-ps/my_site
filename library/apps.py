"""
Configuration for the 'library' Django application.

This module defines the application configuration for the 'library' Django app.
It includes the `LibraryConfig` class, which specifies the default
auto-generated primary key field and the app's name.

The `LibraryConfig` class is used by Django to manage the application's
settings and behavior. It is automatically loaded when the application
is started.

This module is essential for Django to recognize and properly configure
the 'library' app within the project.
"""
from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """
    Configuration for the 'library' Django app.

    This class defines the configuration settings for the 'library' app,
    including the default auto-generated primary key field.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "library"
