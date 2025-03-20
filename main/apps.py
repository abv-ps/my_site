"""
This module contains the configuration for the 'main' app in the Django project.

Classes:
- `HomeConfig`: Configuration for the 'main' app, inheriting from `AppConfig`.

The `HomeConfig` class specifies the default auto field for models in this app and sets the app's name as 'main'.
This configuration is used by Django to set up the app during the project initialization process.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration for the 'main' app.

    This class defines the configuration for the 'main' app in the Django project. It inherits from
    `AppConfig` and specifies settings related to the app's model fields and the app's name.

    Attributes:
        default_auto_field (str): Specifies the default field type for auto-generated primary keys.
        name (str): The name of the app, which is 'main'.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
