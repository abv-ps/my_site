"""
This module provides a utility function for adding the user's avatar URL
to the context for all templates in a Django application.

The function checks if the user is authenticated, retrieves the avatar URL
from the `Profile` model if available, or defaults to a generic avatar image URL
if the user does not have an avatar or is not authenticated.

Modules:
    - django.conf.settings: Provides access to project settings.
    - board.models.Profile: The Profile model, which stores user-specific data,
      including avatars.
    - django.http.HttpRequest: The request object that contains the user information.

Function:
    - avatar_processor(request: HttpRequest) -> Dict[str, str]: Adds the avatar URL
      to the context for templates.
"""

from django.conf import settings
from board.models import Profile
from django.http import HttpRequest
from typing import Dict


def avatar_processor(request: HttpRequest) -> Dict[str, str]:
    """
    Adds the user's avatar URL to the context for all templates.

    If the user is authenticated, it retrieves the avatar URL from the Profile model.
    If the profile does not have an avatar, a default avatar URL is used.
    If the user is not authenticated, the default avatar URL is used.

    Args:
        request (HttpRequest): The HTTP request object, which contains the user.

    Returns:
        Dict[str, str]: A dictionary containing the avatar URL, which can be used
                        in templates.
    """
    default_avatar_url = settings.MEDIA_URL + 'board/avatars/default_avatar25.png'
    avatar_url = default_avatar_url
    print("купи слона")
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            print(f"Profile found: {profile}")
            print(f"начинаем {profile.avatar.url}")
            if profile:
                print(f"Profile avatar field: {profile.avatar}")
                if profile.avatar:
                    avatar_url = profile.avatar.url
                    print(f"User avatar URL: {avatar_url}")
                else:
                    print("User has no avatar, using default.")
            else:
                print("User has no avatar, using default.")
        except Exception as e:
            print(f"Error getting avatar: {e}")

    print(f"Final avatar URL: {avatar_url}")
    return {'avatar_url': avatar_url}
