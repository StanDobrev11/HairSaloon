from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import HairSaloonUser  # Adjust the import based on your model

UserModel = get_user_model()


class HairSaloonUserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name", "phone_number",)


class HairSaloonUserAuthenticationForm(auth_forms.AuthenticationForm):
    username = forms.CharField(label=_("Email or Phone"))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Adjust the query based on your user model fields
            user = HairSaloonUser.objects.filter(email=username).first() or HairSaloonUser.objects.filter(
                phone_number=username).first()
            if user is not None:
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise self.get_invalid_login_error()
                else:
                    self.confirm_login_allowed(self.user_cache)
            else:
                raise ValidationError(_("Invalid login credentials"), code='invalid_login')

        return self.cleaned_data
