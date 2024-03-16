from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from HairSaloon.accounts.forms import HairSaloonUserCreationForm, HairSaloonUserAuthenticationForm


# Create your views here.

class LoginUserView(auth_views.LoginView):
    # this view requires template and 'next' to be used
    # 'next' is defined in settings.py LOGIN_REDIRECT_URL using reverse_lazy
    template_name = 'accounts/login.html'

    # this is needed to redirect the user out of the login page
    redirect_authenticated_user = True


class RegisterUserView(views.CreateView):
    # important here is to use form which is created by the user in forms.py
    form_class = HairSaloonUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
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
        return reverse_lazy('index')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class LogoutUserView(auth_views.LogoutView):

    def get_success_url(self):
        return reverse('index')
