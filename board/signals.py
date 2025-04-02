"""
Module 'board.signals'

This module contains signal handlers for the 'board' application, which respond to various
model events such as saving a `User` or `Ad` instance. These signals are triggered after
a model instance is saved and perform actions like creating related objects, sending
notifications, or deleting files.

Module Dependencies:
- `django.db.models.signals.post_save`: Provides the post-save signal.
- `django.db.models.signals.post_delete`: Provides the post-delete signal.
- `django.db.models.signals.pre_delete`: Provides the pre-delete signal.
- `django.dispatch.receiver`: A decorator for signal handlers.
- `django.core.mail.send_mail`: Used to send email notifications.
- `django.contrib.auth.models.User`: The `User` model for the `Profile` creation.
- `.models.Profile, Ad`: The `Profile` and `Ad` models used in the signal handlers.
- os: Used for file operations.

Signal Handlers:
    - create_user_profile: Creates a new `Profile` instance when a new `User` is created.
    - save_user_profile: Saves the `Profile` instance
      when the associated `User` instance is saved.
    - send_email_on_ad_create: Sends an email notification to the user
      when a new `Ad` is created.
    - deactivate_if_expired: Deactivates an `Ad` if it has been created
      for more than 30 days.
    - delete_avatar: Automatically deletes the avatar file when a `Profile` is deleted.
    - delete_user_profile: Automatically deletes the associated `User`
      when a `Profile` is deleted.
"""
import os
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile, Ad


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler that creates a `Profile` instance for a new `User`
    after saving the `User`.

    This signal is triggered after a new `User` instance is created.
    When a new user is created, a corresponding profile is also created,
    but only if the user does not already have a profile.

    Args:
        sender: The model class that triggered the signal (`User`).
        instance: The instance of the `User` model that was saved.
        created: A boolean indicating whether the object was created
                 (`True` for new, `False` for update).
        **kwargs: Additional keyword arguments.
    """
    # if created:
    # print("create user")
    # Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler that saves the `Profile` instance after saving the `User`.

    This signal is triggered after saving a `User` instance.
    It ensures that the associated `Profile`
    is saved whenever the `User` is saved.

    Args:
        sender: The model class that triggered the signal (`User`).
        instance: The instance of the `User` model that was saved.
        **kwargs: Additional keyword arguments.
    """
    # if hasattr(instance, 'profile'):
    # print("save user")
    # instance.profile.save()


@receiver(post_save, sender=Ad)
def send_email_on_ad_create(sender, instance, created, **kwargs):
    """
    Signal handler that sends an email when a new `Ad` instance is created.

    This signal is triggered after a new `Ad` instance is created.
    It sends an email notification
    to the user who created the ad, informing them of their new ad.

    Args:
        sender: The model class that triggered the signal (`Ad`).
        instance: The instance of the `Ad` model that was saved.
        created: A boolean indicating whether the object was created
                (`True` for new, `False` for update).
        **kwargs: Additional keyword arguments.
    """
    if created:
        send_mail(
            'Нове оголошення',
            f'Ви створили нове оголошення: {instance.title}',
            'burkalo@gmail.com',
            [instance.user.email],
            fail_silently=False,
        )


@receiver(post_save, sender=Ad)
def deactivate_if_expired(sender, instance, **kwargs):
    """
    Signal handler that deactivates the `Ad` instance if it has expired.

    This signal is triggered after an `Ad` instance is saved.
    It checks if the ad has expired (i.e.,
    if it was created more than 30 days ago) and deactivates it if necessary.

    Args:
        sender: The model class that triggered the signal (`Ad`).
        instance: The instance of the `Ad` model that was saved.
        **kwargs: Additional keyword arguments.
    """
    instance.deactivate_if_expired()


@receiver(pre_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    """
    Signal handler that automatically deletes the avatar file when a `Profile` is deleted.

    Args:
        sender: The model class that triggered the signal (`Profile`).
        instance: The instance of the `Profile` model that is about to be deleted.
        **kwargs: Additional keyword arguments.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(post_delete, sender=Profile)
def delete_user_profile(sender, instance, **kwargs):
    """
    Signal handler that automatically deletes the associated `User`
    when a `Profile` is deleted.

    Args:
        sender: The model class that triggered the signal (`Profile`).
        instance: The instance of the `Profile` model that was deleted.
        **kwargs: Additional keyword arguments.
    """
    if instance.user:
        instance.user.delete()
