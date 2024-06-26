from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from HairSaloon.accounts.forms import HairSaloonUserCreationForm, HairSaloonUserPasswordChangeForm, UserAndProfileForm

UserModel = get_user_model()


class LoginUserView(auth_views.LoginView):
    # this view requires template and 'next' to be used
    # 'next' is defined in settings.py LOGIN_REDIRECT_URL using reverse_lazy
    template_name = 'accounts/login.html'

    # this is needed to redirect the user out of the login page
    redirect_authenticated_user = True

    def form_valid(self, form):
        # attempting to clear the messages
        storage = messages.get_messages(self.request)
        storage.used = True
        return super().form_valid(form)

    def form_invalid(self, form):
        # this form handles error msgs upon passing invalid credentials and
        # can be used in the template as {{ messages }} tag
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class RegisterUserView(views.CreateView):
    """
    Newly created user will be handled by this view.

    If user is already registered, the dispatch method will handle the redirection of authenticated users.
    """
    # important here is to use form which is created by the user in forms.py
    form_class = HairSaloonUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())  # not logging sensitive parameters
    @method_decorator(csrf_protect)  # enforces checking of CSRF token before the request is processed
    @method_decorator(never_cache)  # tells browsers not to store sensitive information
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        """
        All new user with never-existing-in-DB email is handled through form_valid(),
        after validation, the user is logged in automatically"""
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    def form_invalid(self, form):
        """
        if user is soft-deleted, they are no longer active, i.e. is_active = False, however, their details are still
        in the DB.
        The email will throw UNIQUE error, hence we need to bypass the email validator. This is done in the
        activate_soft_deleted_user()
        If the user is reactivated, this will redirect to success url and will not continue with form_invalid() method
        """
        reactivated = self.activate_soft_deleted_user(form)
        if reactivated:
            return redirect(self.get_success_url())

        return super().form_invalid(form)

    def activate_soft_deleted_user(self, form):
        try:
            user = UserModel.objects.get(email=form.data.get('email'), is_active=False)
        except UserModel.DoesNotExist:
            return False  # User does not exist or is not inactive

        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.is_active = True
        user.save()

        login(self.request, user)

        return True


class HairSalonEditUserView(LoginRequiredMixin, views.UpdateView):
    model = UserModel
    form_class = UserAndProfileForm
    template_name = 'accounts/edit.html'

    # queryset = UserModel.objects.select_related('hairdresser_profile', 'profile').all()
    # fields = ['first_name', 'last_name', 'phone_number', ]

    def get_success_url(self):
        return reverse_lazy('edit user', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        # Ensure the user can only edit their own profile
        return self.request.user


class HairSalonPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = HairSaloonUserPasswordChangeForm

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('edit user', kwargs={'pk': user.pk})

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request, 'Your password has been updated!')
        return form


class HairSalonDeleteUserView(LoginRequiredMixin, views.DeleteView):
    """
    The method does not actually delete the user but instead sets the is_active attribute to 'False'
    hence preventing the user from logging in.
    """
    template_name = 'accounts/delete_user.html'
    queryset = UserModel.objects.select_related('hairdresser_profile', 'profile').all()
    success_url = reverse_lazy('index')

    def get_object(self, queryset=queryset):
        return queryset.get(pk=self.request.user.pk)

    def form_valid(self, form):
        user = self.request.user
        user.is_active = False
        user.save()
        logout(self.request)
        # messages.success(self.request, 'User deleted')
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return redirect('index')
