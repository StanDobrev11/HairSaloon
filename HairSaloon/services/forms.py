from django import forms
from django.contrib.auth import get_user_model

from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service

UserModel = get_user_model()

class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
#
# class AssignHairdresserFrom(forms.ModelForm):
#     class Meta:
#         model = UserModel
#         fields = '__all__'