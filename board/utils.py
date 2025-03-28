import os
from typing import TYPE_CHECKING

from my_site import settings


if TYPE_CHECKING:
    from django.db.models import Model


def user_avatar_path(instance: "Model", filename: str) -> str:
    """
    Generates the path for saving user avatars inside the respective app's folder.

    Args:
        instance (Model): The model instance containing the image field.
        filename (str): The name of the uploaded file.

    Returns:
        str: The file path where the avatar will be stored.

    Examples:
        >>> class MockInstance:
        ...     class _meta:
        ...         app_label = "board"
        >>> user_avatar_path(MockInstance(), "avatar.jpg")
        'board/media/avatars/avatar.jpg'
    """
    app_label = instance._meta.app_label.lower()
    print(app_label)
    #return os.path.join(settings.MEDIA_ROOT, app_label, filename)
    return os.path.join(app_label, "avatars", filename)
