from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
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


class CreateServiceView(AdminRequiredMixin, views.CreateView):
    """
    The view is accessible for admin users and inherits AdminRequiredMixin

    The admin is responsible for creating/adding new service and assigning it to hairdressers
    """

    template_name = 'services/create_service.html'
    form_class = CreateServiceForm
    success_url = 'list_services'

    def form_valid(self, form):
        hairdressers = form.cleaned_data['select_hairdressers']

        form = form.save(commit=True)
        for hairdresser in hairdressers:
            hairdresser.services.add(form)

        return redirect(self.success_url)

    def get_success_url(self):
        messages.success(self.request, messages.SUCCESS, 'Service created successfully!')
        return reverse_lazy(self.success_url)


class ListServiceView(StaffRequiredMixin, views.ListView):
    """The view is accessible for staff and admin users and inherits StaffRequiredMixin"""

    template_name = 'services/list_services.html'
    queryset = Service.objects.all()
