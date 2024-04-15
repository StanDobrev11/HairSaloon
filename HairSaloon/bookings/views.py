from datetime import timedelta, datetime, date

from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic as views

from HairSaloon.accounts.models import Profile
from HairSaloon.bookings.forms import BookingForm
from HairSaloon.bookings.mixins import DetailViewPermissionMixin
from HairSaloon.bookings.models import Booking


# Create your views here.


class BookingView(auth_mixins.LoginRequiredMixin, views.FormView):
    template_name = 'bookings/dashboard.html'
    form_class = BookingForm
    all_bookings = Booking.objects.select_related('service', 'user', 'hairdresser__user').all()

    # success_url = reverse_lazy('dashboard')
    def set_user_role(self, user_role=None):
        if self.request.user.is_superuser:
            user_role = 'admin'
        elif self.request.user.is_staff:
            user_role = 'staff'
        elif self.request.user.is_authenticated:
            user_role = 'client'

        return user_role

    def get_context_data(self, **kwargs):

        context = super(BookingView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            bookings = self.all_bookings.order_by('date', 'start').filter(cancelled=False)
        elif self.request.user.is_staff:
            bookings = self.all_bookings.order_by('date', 'start').filter(
                hairdresser=self.request.user.hairdresser_profile)
        else:
            bookings = self.all_bookings.order_by('date', 'start').filter(user=self.request.user).exclude(
                cancelled=True)

        context['bookings'] = bookings
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['upcoming_bookings'] = bookings.filter(date__gte=datetime.today())
        context['passed_bookings'] = bookings.filter(date__lt=datetime.today())
        context['user_role'] = self.set_user_role()

        return context

    def get_end_time(self, booking):

        dummy_date = datetime(1, 1, 1)  # Year, month, day
        start_datetime = datetime.combine(dummy_date, booking.start)
        end_datetime = start_datetime + timedelta(minutes=booking.service.duration)

        return end_datetime.time()

    def check_booking_conflicts(self, new_booking, existing_bookings, form):
        """ checks booking conflicts with existing bookings """

        new_booking_hairdresser = new_booking.hairdresser

        if existing_bookings.filter(
                date=new_booking.date,
                end__gte=new_booking.start,
                start__lte=new_booking.end,
                hairdresser=new_booking_hairdresser
        ).exists():
            form.add_error(None, 'Date/Time already taken!')
            return False

        if new_booking.date < date.today():
            form.add_error(None, 'Cannot book in the past!')
            return False

        new_booking_datetime = datetime.combine(new_booking.date, new_booking.start)
        new_booking_datetime = timezone.make_aware(new_booking_datetime, timezone.get_default_timezone())
        current_datetime_plus_60_mins = timezone.now() + timedelta(minutes=60)

        if new_booking_datetime <= current_datetime_plus_60_mins:
            form.add_error(None, 'Booking must be made at least 1 hour in advance.')
            return False

        return True

    def form_valid(self, form):
        new_booking = form.save(commit=False)
        new_booking.user = self.request.user
        new_booking.end = self.get_end_time(new_booking)
        existing_bookings = self.all_bookings.exclude(cancelled=True)

        if not self.check_booking_conflicts(new_booking, existing_bookings, form):
            return self.form_invalid(form)

        if new_booking.user.is_staff:
            # TODO staff logic -> display all bookings, the logged hairdresser in diff colors
            pass

        elif new_booking.user.is_authenticated:
            available_hairdresser = Booking.get_hairdresser(new_booking)

            try:
                new_booking.hairdresser = available_hairdresser[0]
            except IndexError:
                form.add_error(None, 'No hairdresser available for the selected date/time.')
                return self.render_to_response(self.get_context_data(form=form))

        new_booking.initial_user_notified = True
        new_booking.initial_hairdresser_notified = True
        new_booking.save()
        messages.success(self.request, 'Your booking has been successfully created.')
        return self.render_to_response(self.get_context_data(form=self.form_class()))


class BookingDetailView(DetailViewPermissionMixin, views.DetailView):
    template_name = 'bookings/booking_details.html'

    def dispatch(self, request, *args, **kwargs):
        booking = self.get_object()
        kwargs['booking_client'] = booking.user
        kwargs['booking_hairdresser'] = booking.hairdresser
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Booking.objects.get(pk=self.kwargs['pk'])


class BookingDeleteView(DetailViewPermissionMixin, views.DeleteView):
    """ the deletion of the booking should be indicated ONLY by the FALSE in the booking.cancelled field """
    template_name = 'bookings/booking_delete.html'

    def dispatch(self, request, *args, **kwargs):
        booking = self.get_object()
        kwargs['booking_client'] = booking.user
        kwargs['booking_hairdresser'] = booking.hairdresser
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Booking.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        booking = self.get_object()
        booking.cancelled_user_notified = True
        booking.cancelled_hairdresser_notified = True
        booking.cancelled = True
        booking.save()
        messages.success(self.request, 'Booking cancelled')
        return HttpResponseRedirect('/dashboard/')
