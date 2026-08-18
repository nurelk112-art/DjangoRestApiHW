from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def test_task():
    return "Celery работает!"


@shared_task
def scheduled_task():
    print(f"Запланированная задача выполнена: {timezone.now()}")


@shared_task
def send_test_email():
    send_mail(
        subject="Тест Celery + SMTP",
        message="Письмо успешно отправлено через Celery и SMTP!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
    )

    return "Email sent successfully!"
