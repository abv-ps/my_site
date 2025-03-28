import os
import uuid
from typing import TYPE_CHECKING

#from board.models import Profile
from my_site import settings


if TYPE_CHECKING:
    from django.db.models import Model


def get_avatar_upload_path(instance: "Model", filename: str) -> str:
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
        'board/avatars/avatar.jpg'
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('board', 'avatars', str(instance.profile.id), unique_filename)

def get_default_avatar():
    return os.path.join('board', 'avatars', 'default_avatar.png')