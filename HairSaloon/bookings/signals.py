
# TODO trigger that notifies user and hairdresser for creation of the booking
# TODO trigger that notifies user and hairdresser for alteration of the booking
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from HairSaloon.bookings.models import Booking


@receiver(pre_delete, sender=Booking)
def delete_booking(sender, instance, **kwargs):
    """ the signal triggers notification for the cancellation of the user and the hairdresser"""
    # TODO trigger that notifies user and hairdresser for the cancellation of the booking
