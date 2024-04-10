from django import forms

from HairSaloon.bookings.models import Booking
from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service


#
#
# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['date', 'start', 'end', 'service', 'notes']
#
#         widgets = {
#             'date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
#         }

class BookingForm(forms.ModelForm):
    hairdresser = forms.ModelChoiceField(queryset=HairDresser.objects.all(), required=True)

    class Meta:
        model = Booking
        fields = ['hairdresser', 'date', 'start', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.none()

        if 'hairdresser' in self.data:
            try:
                hairdresser_id = int(self.data.get('hairdresser'))
                self.fields['service'].queryset = Service.objects.filter(hairdressers__id=hairdresser_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Service queryset
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.hairdresser.services.order_by('name')