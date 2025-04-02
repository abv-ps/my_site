"""
Module 'board.models'

This module defines the models for the 'board' application in Django, which include:
- Profile: Represents the user profile with additional user information.
- Category: Represents an advertisement category.
- Ad: Represents an advertisement with details such as title, description, price, and category.
- Comment: Represents a comment on an advertisement.

Module Dependencies:
- `django.contrib.auth.models.User`: The User model used to associate users with profiles and ads.
- `django.db.models`: Used to define models and fields for the database.
- `django.utils.timezone`: Provides timezone utilities, including the current time.
- `datetime.timedelta`: Used to handle date calculations for ad expiration.
- `django.core.exceptions.ValidationError`: Used for custom model validation.
- `os`: Used for file path operations.
- `uuid`: Used for generating unique filenames.
- `.validators.validate_phone_number`: Custom validator for phone numbers.
- `.validators.validate_avatar_image`: Custom validator for avatar images.

Models:
    - Profile: Stores additional information about the user such as phone number,
      address, and email.
    - Category: Stores information about advertisement categories and their descriptions.
    - Ad: Stores advertisements, including details such as title, description, price,
      creation date, and category.
    - Comment: Stores user comments on advertisements.

Each model provides various methods for managing the data, including string representations,
validation methods, and helper functions.
"""
import os
import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from .validators import validate_phone_number, validate_avatar_image


def get_avatar_upload_path(instance: "Profile", filename: str) -> str:
    """
    Generates the path for saving user avatars inside the respective app's folder.

    Args:
        instance: The model instance containing the image field.
        filename: The name of the uploaded file.

    Returns:
        The file path where the avatar will be stored.
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('board', 'avatars', str(instance.user.id), unique_filename)


def get_default_avatar() -> str:
    """
    Returns the default avatar path.

    Returns:
        The default avatar path.
    """
    return os.path.join('board', 'avatars', 'default_avatar.png')


class Profile(models.Model):
    """
    A model representing a user profile.

    This model is associated with the `User` model and contains additional
    information about a user such as phone number, address, email, bio,
    birth date, and user status (whether the user is active or a staff member).

    Attributes:
        user (OneToOneField): A one-to-one relationship with the `User` model,
                              representing the associated user.
        bio (TextField): A short biography or description of the user (optional).
        phone_number (CharField): The user's phone number (optional).
        birth_date (DateField): The user's birth date (optional).
        location (CharField): The user's address or location (optional).
        email (EmailField): The user's email address (optional).
        is_active (BooleanField): Whether the user's profile is active (default: True).
        is_staff (BooleanField): Whether the user is a staff member (default: False).
        avatar (ImageField): The user's avatar image.

    Methods:
        __str__: Returns a string representation of the profile, showing the user's username.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True,
                                    validators=[validate_phone_number])
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=get_avatar_upload_path, blank=True,
                               null=True, default=get_default_avatar,
                               validators=[validate_avatar_image])

    def __str__(self) -> str:
        """
        Returns a string representation of the profile.

        This method returns the username of the associated user for easy
        identification of the profile.

        Returns:
            The username of the associated user.
        """
        return f'{self.user.username} Profile'


class Category(models.Model):
    """
    A model representing a category for advertisements.

    This model holds information about the category's name and description
    and provides a method to get the count of active ads in that category.

    Attributes:
        name (CharField): The name of the category (must be unique).
        description (TextField): A description of the category.

    Methods:
        get_active_ads_count:
            Returns the count of active ads in this category.

        __str__:
            Returns a string representation of the category's name.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def get_active_ads_count(self) -> int:
        """
        Gets the count of active ads in this category.

        Returns:
            int: The count of active ads in the category.
        """
        return self.ad_set.filter(is_active=True).count()

    def __str__(self) -> str:
        """
        String representation of the Category model.

        Returns:
           str: The name of the category.
        """
        return str(self.name)


class Ad(models.Model):
    """
    A model representing an advertisement.

    This model contains information about the ad such as title, description,
    price, creation date, and category, and provides methods for description
    truncation, deactivating expired ads, and validating the price.

    Attributes:
        title (CharField): The title of the ad.
        description (TextField): A detailed description of the ad.
        price (DecimalField): The price of the item or service being advertised.
        created_at (DateTimeField): The date and time when the ad was created.
        updated_at (DateTimeField): The date and time when the ad was last updated.
        is_active (BooleanField): Whether the ad is active.
        user (ForeignKey): The user who posted the ad.
        category (ForeignKey): The category to which the ad belongs.

    Methods:
        short_description:
            Returns the first 100 characters of the description.

        deactivate_if_expired:
            Deactivates the ad if it has been created more than 30 days ago.

        clean:
            Validates the price of the ad to ensure it is greater than zero.

        __str__:
            Returns a string representation of the ad's title.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def short_description(self) -> str:
        """
        Returns the first 100 characters of the ad's description.

        Returns:
            str: The truncated description (first 100 characters).
        """
        return str(self.description[:100])

    def deactivate_if_expired(self) -> None:
        """
        Deactivates the ad if it has been created more than 30 days ago.

        This method checks if the ad's creation date is older than 30 days
        and sets the ad's `is_active` status to False if it is.
        """
        if self.created_at + timedelta(days=30) < timezone.now():
            self.is_active = False
            self.save()

    def clean(self) -> None:
        """
        Validates the price to ensure it is a positive value.

        Raises:
            ValidationError: If the price is less than or equal to zero.
        """
        if self.price <= 0:
            raise ValidationError("Ціна має бути додатним числом.")

    def __str__(self) -> str:
        """
        String representation of the Ad model.

        Returns:
            str: The title of the ad.
        """
        return str(self.title)


class Comment(models.Model):
    """
    A model representing a comment on an advertisement.

    This model holds the content of the comment, the date it was created,
    and the associated ad and user.

    Attributes:
        content (TextField): The text content of the comment.
        created_at (DateTimeField): The date and time when the comment was created.
        ad (ForeignKey): The ad that the comment is associated with.
        user (ForeignKey): The user who posted the comment.

    Methods:
        __str__:
            Returns a string representation of the comment's content, truncated to 50 characters.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        String representation of the Comment model.

        Returns:
            str: The first 50 characters of the comment content.
        """
        return str(self.content[:50])
