from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_async_email(email, created_at):
    send_mail(
        subject=f'Booking created at {created_at}',
        message='Booking created successfully',
        from_email='hair@saloon.com',
        recipient_list=[email],
        fail_silently=False,
    )
