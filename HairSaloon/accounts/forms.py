from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

UserModel = get_user_model()


class HairSaloonUserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name", "phone_number",)
