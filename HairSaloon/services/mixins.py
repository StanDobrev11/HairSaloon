from django.contrib.auth import mixins as auth_mixins


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
