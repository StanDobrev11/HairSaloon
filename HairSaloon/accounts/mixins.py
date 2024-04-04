from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect


class BasePermissionMixin(auth_mixins.AccessMixin):
    """A mixin that grants access to users based on their role and if they are active."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Login first to view the page')
            return self.handle_no_permission()

        # if not request.user.is_active:
        #     return self.handle_no_permission()
        #
        # # Check for admin access
        # if hasattr(self, 'admin_required') and self.admin_required:
        #     if not request.user.is_superuser:
        #         return self.handle_no_permission()
        #
        # # Check for staff access
        # if hasattr(self, 'staff_required') and self.staff_required:
        #     if not request.user.is_staff:
        #         return self.handle_no_permission()
        #
        # if messages:
        #     list(messages.get_messages(request))
        return super().dispatch(request, *args, **kwargs)


class DetailViewPermissionMixin(BasePermissionMixin):

    def dispatch(self, request, *args, **kwargs):
        booking_client = kwargs.get('booking_client', None)

        if not request.user == booking_client:
            messages.error(request, 'You have no access to view this booking details')
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)
