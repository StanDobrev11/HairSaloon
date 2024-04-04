from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.forms import CreateServiceForm
from HairSaloon.services.mixins import StaffRequiredMixin, AdminRequiredMixin, FormValidMixin
from HairSaloon.services.models import Service

UserModel = get_user_model()


class DetailServiceView(views.DetailView):
    """The view is accessible for all user and provide details about a service"""

    queryset = Service.objects.all()
    template_name = 'services/details_service.html'

    def get_object(self, queryset=queryset):
        return queryset.get(pk=self.kwargs['pk'])


class CreateServiceView(AdminRequiredMixin, views.CreateView):
    """
    The view is accessible for admin users and inherits AdminRequiredMixin

    The admin is responsible for creating/adding new service and assigning it to hairdressers
    """

    template_name = 'services/create_service.html'
    form_class = CreateServiceForm
    success_url = 'list_services'

    def form_valid(self, form):
        """when the method is called, the service is assigned to the selected hairdressers"""
        hairdressers = form.cleaned_data['select_hairdressers']

        form = form.save(commit=True)
        for hairdresser in hairdressers:
            hairdresser.services.add(form)

        return redirect(self.success_url)

    def get_success_url(self):
        """the message is not used"""
        messages.success(self.request, messages.SUCCESS, 'Service created successfully!')
        return reverse_lazy(self.success_url)


class ListServiceView(StaffRequiredMixin, views.ListView):
    """The view is accessible for staff and admin users and inherits StaffRequiredMixin"""

    template_name = 'services/list_services.html'
    queryset = Service.objects.all()


class DeleteServiceView(AdminRequiredMixin, views.DeleteView):
    model = Service
    success_url = reverse_lazy('list_services')
    template_name = 'services/delete_service.html'

    def get_object(self, queryset=None):
        return Service.objects.get(pk=self.kwargs['pk'])


class EditServiceView(AdminRequiredMixin, views.UpdateView):
    """
    CreateServiceForm will be used to edit a service.

    For this to work, hairdressers, able to perform the service, must be passed to the form.
    The best place to pass additional arguments to the form is the get_form_kwargs() method.

    The form_valid() method must be overwritten to assign service to newly selected hairdressers
    and at the same tame checks if a hairdresser cannot perform the service anymore.
    """
    template_name = 'services/edit_service.html'
    form_class = CreateServiceForm
    success_url = reverse_lazy('list_services')

    def get_object(self, queryset=None):
        return Service.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service = self.get_object()
        kwargs['initial'] = {'select_hairdressers': service.hairdressers.all()}
        return kwargs

    def form_valid(self, form):
        """
        When the method is called, the service is assigned to the selected hairdressers
        if there are hairdressers that are not selected after the edit, the service should be removed
        from their list.
        """
        hairdressers = form.cleaned_data['select_hairdressers']

        form = form.save(commit=True)
        form.hairdressers.clear()

        for hairdresser in hairdressers:
            hairdresser.services.add(form)

        return redirect(self.success_url)
