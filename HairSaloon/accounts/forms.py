from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class HairSaloonUserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name", "phone_number",)


# class HairSaloonUserEditForm(auth_forms.UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["email"].widgets.attrs['readonly'] = True
#
#     class Meta:
#         model = UserModel
#         fields = ("email", "phone_number", "first_name", "last_name",)


class HairSaloonUserPasswordChangeForm(auth_forms.PasswordChangeForm):
    class Meta:
        model = UserModel
        fields = ("old_password", "new_password1", "new_password2")

    def save(self, commit=True):
        return super().save()
