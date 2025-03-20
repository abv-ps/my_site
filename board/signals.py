from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile, Ad

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Ad)
def send_email_on_ad_create(sender, instance, created, **kwargs):
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
    instance.deactivate_if_expired()
