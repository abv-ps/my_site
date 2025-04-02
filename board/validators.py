"""
Module 'board.validators'

This module provides custom validators for various data types used in the bulletin
board application, including image files and phone numbers.

Key Functions:

- **validate_avatar_image**: Validates uploaded avatar images, ensuring they are of
  the correct file type (png, jpg, jpeg) and do not exceed a maximum size of 3 MB.

- **validate_phone_number**: Validates phone numbers, ensuring they are in a valid
  format and are valid for the specified country.

Dependencies:
- os
- phonenumbers
- django.core.exceptions
- django.utils.translation
- django.core.files.uploadedfile
"""

import os
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_avatar_image(file: InMemoryUploadedFile):
    """
    Custom validator to check file type and size for avatar.
    Only allows png, jpg, jpeg file types, and a maximum size of 3 MB.

    Args:
        file: The uploaded image file.

    Raises:
        ValidationError: If the file type is invalid or the file size exceeds 3 MB.
    """
    ext = os.path.splitext(file.name)[1].lower()[1:]
    valid_extensions = ['png', 'jpg', 'jpeg']
    if ext not in valid_extensions:
        raise ValidationError(_('Only files with extensions: png, jpg, jpeg.'))

    max_size_mb = 3 * 1024 * 1024
    if file.size > max_size_mb:
        raise ValidationError(_('File size cannot exceed 3 MB.'))


def validate_phone_number(value: str):
    """
    Validates a phone number to ensure it is in a valid format and is valid for
    the specified country.

    Args:
        value: The phone number string to validate.

    Raises:
        ValidationError: If the phone number is invalid or not in a valid format.
    """
    try:
        phone_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(_("The phone number is invalid. "
                                    "Please make sure it follows the correct format "
                                    "and is valid for the country."
                                    "(like '+380961231122')."))
    except NumberParseException as exc:
        raise ValidationError(_("The phone number is not in a valid format. "
                                "Please make sure it includes the country code "
                                "and the correct number of digits"
                                "(like '+380961231122').")) from exc
