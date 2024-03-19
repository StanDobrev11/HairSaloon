from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your models here.


from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service

UserModel = get_user_model()


def bookings_directory_path(instance, filename=None):
    # file will be uploaded to MEDIA_ROOT/bookings/user_<id>/<filename>
    return 'bookings/user_{0}/'.format(instance.user.pk)


class Booking(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    user_notified = models.BooleanField(default=False)
    hairdresser_notified = models.BooleanField(default=False)
    pre_photo = models.ImageField(
        upload_to=bookings_directory_path,
        blank=True,
    )
    post_photo = models.ImageField(
        upload_to=bookings_directory_path,
        blank=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    hairdresser = models.ForeignKey(
        to=HairDresser,
        on_delete=models.CASCADE,
        related_name='bookings',
    )

    def get_hairdresser(self):
        """
        this method get available hairdresser based on date/time of the booking and service required
        """
        capable_hairdressers = HairDresser.objects.filter(services__id=self.service.id)
        available_hairdressers = []

        for hairdresser in capable_hairdressers:
            # Check if the hairdresser has bookings that conflict with the requested time.
            conflicting_bookings = hairdresser.bookings.filter(
                date=self.date, start__lt=self.end, end__gt=self.start)

            # If there are no conflicting bookings, the hairdresser is available.
            if not conflicting_bookings.exists():
                available_hairdressers.append(hairdresser)

        return available_hairdressers

    class Meta:
        ordering = ['-date', '-start']

    def __str__(self):
        return f"Booking for {self.user} with {self.hairdresser} for {self.service}"
