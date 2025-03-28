import os
import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_avatar_image(file: InMemoryUploadedFile):
    """
    Custom validator to check file type and size for avatar.
    Only allows png, jpg, jpeg file types, and a maximum size of 3 MB.
    """
    ext = os.path.splitext(file.name)[1].lower()[1:]
    valid_extensions = ['png', 'jpg', 'jpeg']
    if ext not in valid_extensions:
        raise ValidationError(_('Тільки файли з розширеннями: png, jpg, jpeg.'))

    max_size_mb = 3 * 1024 * 1024
    if file.size > max_size_mb:
        raise ValidationError(_('Розмір файлу не може перевищувати 3 МБ.'))

def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(_("The phone number is invalid. "
                                    "Please make sure it follows the correct format "
                                    "and is valid for the country."
                                    "(like '+380961231122')."))
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(_("The phone number is not in a valid format. "
                                "Please make sure it includes the country code "
                                "and the correct number of digits"
                                "(like '+380961231122')."))