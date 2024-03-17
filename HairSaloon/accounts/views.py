from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from HairSaloon.accounts.forms import HairSaloonUserCreationForm

UserModel = get_user_model()


# Create your views here.

class LoginUserView(auth_views.LoginView):
    # this view requires template and 'next' to be used
    # 'next' is defined in settings.py LOGIN_REDIRECT_URL using reverse_lazy
    template_name = 'accounts/login.html'

    # this is needed to redirect the user out of the login page
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # this form handles error msgs upon passing invalid credentials and
        # can be used in the template as {{ messages }} tag
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


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


class ProfileUserView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    # model = UserModel
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = UserModel.objects.get(pk=self.request.user.pk)
        return context


def logout_view(request):
    logout(request)

    return redirect('index')
