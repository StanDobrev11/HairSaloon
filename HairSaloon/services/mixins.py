from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect


class StaffRequiredMixin(auth_mixins.LoginRequiredMixin):
    raise_exception = True
    permission_denied_message = 'No permissions to access this resource!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(StaffRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        """when the method is called, the service is assigned to the selected hairdressers"""
        hairdressers = form.cleaned_data['select_hairdressers']

        form = form.save(commit=True)
        for hairdresser in hairdressers:
            hairdresser.services.add(form)

        return redirect(self.success_url)
