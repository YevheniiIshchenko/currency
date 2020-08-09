from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings


@shared_task
def send_message(data: dict):

    send_mail(
        data['title'],
        data['message'],
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
