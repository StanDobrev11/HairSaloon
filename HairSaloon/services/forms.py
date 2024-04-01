from django import forms
from django.contrib.auth import get_user_model

from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service

UserModel = get_user_model()


class CreateServiceForm(forms.ModelForm):
    select_hairdressers = forms.ModelMultipleChoiceField(
        queryset=HairDresser.objects.all(),
    )

    class Meta:
        model = Service
        fields = '__all__'
