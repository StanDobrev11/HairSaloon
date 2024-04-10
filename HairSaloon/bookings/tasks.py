from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_async_email_new_booking(user_email, hairdresser_email, created_at):
    send_mail(
        subject=f'Booking created at {created_at}',
        message='Booking created successfully',
        from_email='hair@saloon.com',
        recipient_list=[user_email, hairdresser_email],
        fail_silently=False,
    )


@shared_task
def send_async_email_cancelled_booking(user_email, hairdresser_email, created_at):
    send_mail(
        subject=f'Booking {created_at} cancelled',
        message='Booking cancelled successfully',
        from_email='hair@saloon.com',
        recipient_list=[user_email, hairdresser_email],
        fail_silently=False,
    )
