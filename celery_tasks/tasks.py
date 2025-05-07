from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task
def send_registration_email(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        'Реєстрація успішна!',
        'Вітаємо, ви успішно зареєструвалися на нашому сервісі.',
        'noreply@example.com',
        [user.email],
    )
    logger.info(f'Email про реєстрацію надіслано користувачу: {user.email}')


@shared_task
def send_advertisement_email(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        'Можливості сервісу',
        'Перегляньте наші можливості: оголошення, пошук, фільтри і багато іншого!',
        'noreply@example.com',
        [user.email],
    )
    logger.info(f'Рекламний email надіслано користувачу: {user.email}')


@shared_task
def log_total_users():
    total = User.objects.count()
    logger.info(f'Кількість користувачів у системі: {total}')
