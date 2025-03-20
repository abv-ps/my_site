"""
This module contains signal handlers for the 'board' application, which respond to various
model events such as saving a `User` or `Ad` instance. These signals are triggered after
a model instance is saved and perform actions like creating related objects or sending notifications.

Module Dependencies:
- `django.db.models.signals.post_save`: Provides the post-save signal.
- `django.dispatch.receiver`: A decorator for signal handlers.
- `django.core.mail.send_mail`: Used to send email notifications.
- `django.contrib.auth.models.User`: The `User` model for the `Profile` creation.
- `.models.Profile, Ad`: The `Profile` and `Ad` models used in the signal handlers.

Signal Handlers:
    - create_user_profile: Creates a new `Profile` instance when a new `User` is created.
    - save_user_profile: Saves the `Profile` instance when the associated `User` instance is saved.
    - send_email_on_ad_create: Sends an email notification to the user when a new `Ad` is created.
    - deactivate_if_expired: Deactivates an `Ad` if it has been created for more than 30 days.

"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile, Ad


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler that creates a `Profile` instance for a new `User` after saving the `User`.

    This signal is triggered after a new `User` instance is created. When a new user is created,
    a corresponding profile is also created.

    Args:
        sender (class): The model class that triggered the signal (`User`).
        instance (User): The instance of the `User` model that was saved.
        created (bool): A boolean indicating whether the object was created (`True` for new, `False` for update).
        **kwargs: Additional keyword arguments.

    Methods:
        None
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler that saves the `Profile` instance after saving the `User`.

    This signal is triggered after saving a `User` instance. It ensures that the associated `Profile`
    is saved whenever the `User` is saved.

    Args:
        sender (class): The model class that triggered the signal (`User`).
        instance (User): The instance of the `User` model that was saved.
        **kwargs: Additional keyword arguments.

    Methods:
        None
    """
    instance.profile.save()


@receiver(post_save, sender=Ad)
def send_email_on_ad_create(sender, instance, created, **kwargs):
    """
    Signal handler that sends an email when a new `Ad` instance is created.

    This signal is triggered after a new `Ad` instance is created. It sends an email notification
    to the user who created the ad, informing them of their new ad.

    Args:
        sender (class): The model class that triggered the signal (`Ad`).
        instance (Ad): The instance of the `Ad` model that was saved.
        created (bool): A boolean indicating whether the object was created (`True` for new, `False` for update).
        **kwargs: Additional keyword arguments.

    Methods:
        send_mail:
            Sends an email notification to the user about their new ad.
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

    This signal is triggered after an `Ad` instance is saved. It checks if the ad has expired (i.e.,
    if it was created more than 30 days ago) and deactivates it if necessary.

    Args:
        sender (class): The model class that triggered the signal (`Ad`).
        instance (Ad): The instance of the `Ad` model that was saved.
        **kwargs: Additional keyword arguments.

    Methods:
        deactivate_if_expired:
            Deactivates the ad if it has expired.
    """
    instance.deactivate_if_expired()
