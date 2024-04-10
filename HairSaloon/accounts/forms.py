from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

from HairSaloon.accounts.models import Profile

UserModel = get_user_model()


class HairSaloonUserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name", "phone_number",)


class HairSaloonUserPasswordChangeForm(auth_forms.PasswordChangeForm):
    class Meta:
        model = UserModel
        fields = ("old_password", "new_password1", "new_password2")

    def save(self, commit=True):
        return super().save()


class UserAndProfileForm(forms.ModelForm):
    # Add fields from the Profile model here
    account_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'phone_number', 'account_photo', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        # Initialize form with instance data if available
        super(UserAndProfileForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['account_photo'].initial = self.instance.profile.account_photo
            self.fields['date_of_birth'].initial = self.instance.profile.date_of_birth

    def save(self, commit=True):
        # Save the user model
        user = super(UserAndProfileForm, self).save(commit=False)
        if commit:
            user.save()
            # Save or update the profile model
            profile, created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'account_photo': self.cleaned_data.get('account_photo', None),
                    'date_of_birth': self.cleaned_data.get('date_of_birth', None),
                }
            )
        return user
