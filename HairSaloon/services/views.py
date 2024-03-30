from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.forms import CreateServiceForm
from HairSaloon.services.mixins import StaffRequiredMixin, AdminRequiredMixin
from HairSaloon.services.models import Service

UserModel = get_user_model()


class DetailServiceView(views.DetailView):
    """The view is accessible for all user"""

    queryset = Service.objects.all()
    template_name = 'partials/../../templates/services/details_service.html'

    def get_object(self, queryset=queryset):
        return queryset.get(pk=self.kwargs['pk'])


class CreateServiceView(StaffRequiredMixin, views.CreateView):
    """
    The view is accessible for staff and admin users and inherits StaffRequiredMixin

    If the user creating the service is a hairdresser, then the service will be auto associated with
    the user

    If the user is admin, then will be redirected to page to associate the service to hairdressers

    """

    template_name = 'services/create_service.html'
    form_class = CreateServiceForm
    success_url = 'list_services'

    def form_valid(self, form):

        try:
            hairdresser = HairDresser.objects.get(pk=self.request.user.hairdresser_profile.pk)
        except HairDresser.DoesNotExist:
            return self.form_invalid(form)

        form = form.save(commit=True)

        if self.request.user.is_superuser:
            self.success_url = 'assign_hairdresser'
        else:
            hairdresser.services.add(form)

        return redirect(self.success_url)

    def get_success_url(self):
        messages.success(self.request, messages.SUCCESS, 'Service created successfully!')
        return reverse_lazy(self.success_url)


class ServiceToHairdresserAssociationView(AdminRequiredMixin, views.CreateView):
    """
    The view is accessible for admin users ONLY and inherits StaffRequiredMixin

    Provides options to assign hairdresser to the newly created service.

    The admin has the option to assign the service to one or more hairdressers.
    """

    template_name = 'services/hairdresser_to_service.html'
    queryset = UserModel.hairdresser_profile
    fields = "__all__"


def get_success_url(self):
    messages.success(self.request, messages.SUCCESS, 'Service assigned successfully!')
    return reverse_lazy('list_services')


class ListServiceView(StaffRequiredMixin, views.ListView):
    """The view is accessible for staff and admin users and inherits StaffRequiredMixin"""

    template_name = 'services/list_services.html'
    queryset = Service.objects.all()
