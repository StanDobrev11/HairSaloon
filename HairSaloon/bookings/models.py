from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service

UserModel = get_user_model()


class Booking(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    user_notified = models.BooleanField(default=False)
    hairdresser_notified = models.BooleanField(default=False)

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
        related_name='bookings'
    )

    def save(self, *args, **kwargs):
        duration = self.service.duration
        self.end = self.start + timedelta(minutes=duration)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-start']

    def __str__(self):
        return f"Booking for {self.user} with {self.hairdresser} for {self.service}"
