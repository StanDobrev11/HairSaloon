from django import forms

from HairSaloon.bookings.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start', 'end', 'service', 'notes']

        widgets = {
            'date': forms.DateInput(format='%d.%m.%Y', attrs={'type': 'date'}),
        }

