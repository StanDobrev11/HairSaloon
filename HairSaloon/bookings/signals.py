from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking
from .tasks import send_async_email_new_booking, send_async_email_cancelled_booking  # Import the Celery task


@receiver(post_save, sender=Booking)
def create_booking(sender, instance, created, **kwargs):
    """sending emails to the client and to the hairdresser"""
    if created:
        task_kwargs = {
            'user_email': instance.user.email,
            'hairdresser_email': instance.hairdresser.user.email,
            'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        instance.initial_user_notified = True
        instance.initial_hairdresser_notified = True
        send_async_email_new_booking.delay(**task_kwargs)


@receiver(post_save, sender=Booking)
def cancel_booking(sender, instance, **kwargs):
    if instance.cancelled:
        task_kwargs = {
            'user_email': instance.user.email,
            'hairdresser_email': instance.hairdresser.user.email,
            'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        instance.cancelled_user_notified = True
        instance.cancelled_hairdresser_notified = True
        send_async_email_cancelled_booking.delay(**task_kwargs)
