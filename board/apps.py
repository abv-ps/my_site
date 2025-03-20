"""
This module contains the configuration for the 'board' Django application.

The `BoardConfig` class is used to configure the app, set the default field type
for primary keys, and import the necessary signals.

Module Dependencies:
- `django.apps.AppConfig`: Used to configure the 'board' app.
- `board.signals`: Used to import and register signals for the application.

Attributes:
    BoardConfig:
        - default_auto_field: Defines the default primary key field type.
        - name: The name of the app within the Django project.

Module Functions:
    - ready: A method in `BoardConfig` that ensures signals are properly imported
      when the application is ready.
"""
from django.apps import AppConfig


class BoardConfig(AppConfig):
    """
    Configuration class for the 'board' application.

    This class is used to configure the 'board' app, including setting the default
    auto field for model primary keys and importing any signals for the app.

    Attributes:
        default_auto_field (str): The default field type for primary keys in models.
        name (str): The name of the application. Used by Django to identify the app.

    Methods:
        ready:
            Args:
                self (BoardConfig): The instance of the BoardConfig class.

            This method is called when the application is ready,
            and it's used to import signals for the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'

    def ready(self):
        """
        The method called when the application is ready.

        This method imports the `signals` module of the 'board' app to ensure
        that any signal handlers are registered when the app is ready.

        Args:
            self (BoardConfig): The instance of the BoardConfig class.
        """
        import board.signals
