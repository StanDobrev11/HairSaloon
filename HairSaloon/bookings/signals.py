from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from .tasks import send_async_email  # Import the Celery task


@receiver(post_save, sender=Booking)
def create_booking(sender, instance, created, **kwargs):
    if created:
        task_kwargs = {
            'email': instance.user.email,
            'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        send_async_email.delay(**task_kwargs)
