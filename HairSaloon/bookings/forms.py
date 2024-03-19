from django import forms

from HairSaloon.bookings.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start', 'end', 'service', 'notes']
