import os
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