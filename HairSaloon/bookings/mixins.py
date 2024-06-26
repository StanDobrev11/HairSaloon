from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect


class BasePermissionMixin(auth_mixins.AccessMixin):
    """A mixin that grants access to users based on their role and if they are active."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Login first to view the page')
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class DetailViewPermissionMixin(BasePermissionMixin):

    def dispatch(self, request, *args, **kwargs):
        booking_client = kwargs.get('booking_client', None)
        booking_hairdresser = kwargs.get('booking_hairdresser', None)

        if request.user.is_superuser or request.user == booking_client or request.user.hairdresser_profile == booking_hairdresser:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, 'You have no access to view this booking details')
        return redirect('dashboard')
