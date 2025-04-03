from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Book

@receiver(post_delete, sender=User)
def update_books_on_user_delete(sender, instance, **kwargs):
    Book.objects.filter(updated_by=instance.username).update(
        updated_by=f"{instance.username} (видалено)"
    )