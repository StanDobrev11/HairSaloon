from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from HairSaloon.bookings.models import Booking


@receiver(post_save, sender=Booking)
def create_booking(sender, instance, created, **kwargs):
    if created:
        email = instance.user.email
        send_mail(
            'Booking created',
            'Booking created successfully',
            'hair@saloon.com',
            [f"{email}"],
            fail_silently=False,
        )
