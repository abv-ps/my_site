"""
This module provides a utility function for adding the user's avatar URL
to the context for all templates in a Django application.

The function checks if the user is authenticated, retrieves the avatar URL
from the user's profile if available, or defaults to a generic avatar image URL
if the user does not have an avatar or is not authenticated.

Modules:
    - django.conf.settings: Provides access to project settings.
    - django.http.HttpRequest: The request object that contains the user information.

Function:
    - avatar_processor(request: HttpRequest) -> Dict[str, str]: Adds the avatar URL
      to the context for templates.
"""
import os
from typing import Dict

from django.http import HttpRequest

from my_site import settings
from logger_config import get_logger

logger = get_logger(__name__, "context_processors.log")


def avatar_processor(request: HttpRequest) -> Dict[str, str]:
    """
    Adds the user's avatar URL to the context for all templates.

    If the user is authenticated, it retrieves the avatar URL from the user's profile.
    If the profile does not have an avatar, a default avatar URL is used.
    If the user is not authenticated, the default avatar URL is used.

    Args:
        request (HttpRequest): The HTTP request object, which contains the user.

    Returns:
        Dict[str, str]: A dictionary containing the avatar URL, which can be used
                        in templates.
    """

    default_avatar_url = os.path.join('board', 'default_avatar.png')

    avatar_url = f"{settings.MEDIA_URL}{default_avatar_url}"
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile and profile.avatar:
                avatar_url = profile.avatar.url
                logger.info("User avatar URL: %s", avatar_url)
            else:
                logger.warning("User has no avatar or profile, using default.")
        except AttributeError:
            logger.warning("User has no profile, using default avatar.")
        except Exception as e:
            logger.error("Error getting avatar: %s", str(e))

    return {'avatar_url': avatar_url}
