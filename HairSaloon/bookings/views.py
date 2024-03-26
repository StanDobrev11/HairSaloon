from datetime import timedelta, datetime, date
from django.contrib import messages
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views import generic as views

from HairSaloon.accounts.models import Profile
from HairSaloon.bookings.forms import BookingForm
from HairSaloon.bookings.models import Booking


# Create your views here.


class BookingView(views.FormView):
    template_name = 'bookings/dashboard.html'
    form_class = BookingForm

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
        bookings = Booking.objects.all().prefetch_related()
        context['bookings'] = bookings
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['upcoming_bookings'] = bookings.filter(date__gte=datetime.today(), user=self.request.user)
        context['passed_bookings'] = bookings.filter(date__lte=datetime.today(), user=self.request.user)
        context['user_role'] = self.set_user_role()

        return context

    def get_end_time(self, booking):

        dummy_date = datetime(1, 1, 1)  # Year, month, day
        start_datetime = datetime.combine(dummy_date, booking.start)
        end_datetime = start_datetime + timedelta(minutes=booking.service.duration)

        return end_datetime.time()

    def check_booking_conflicts(self, new_booking, all_bookings, form):
        """ checks booking conflicts with existing bookings """

        if all_bookings.filter(date=new_booking.date, end__gte=new_booking.start, start__lte=new_booking.end).exists():
            form.add_error(None, 'Date/Time already taken!')
            return False

        if new_booking.date < date.today():
            form.add_error(None, 'Cannot book in the past!')
            return False

        if new_booking.date == date.today() and new_booking.start <= timezone.now() + timedelta(minutes=60):
            form.add_error(None, 'Booking must be made at least 1 hour in advance.')
            return False

        return True

    def form_valid(self, form):
        new_booking = form.save(commit=False)
        new_booking.user = self.request.user
        new_booking.end = self.get_end_time(new_booking)
        all_bookings = Booking.objects.prefetch_related()

        if not self.check_booking_conflicts(new_booking, all_bookings, form):
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

        new_booking.save()
        messages.success(self.request, 'Your booking has been successfully created.')
        return self.render_to_response(self.get_context_data(form=self.form_class()))


class BookingDetailView(views.DetailView):
    template_name = 'bookings/booking_details.html'

    def get_object(self, queryset=None):
        return Booking.objects.get(pk=self.kwargs['pk'])


class BookingDeleteView(views.DeleteView):
    template_name = 'bookings/booking_delete.html'

    def get_object(self, queryset=None):
        return Booking.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('dashboard')
