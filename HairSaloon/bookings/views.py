from datetime import timedelta, datetime
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic as views

from HairSaloon.accounts.models import Profile
from HairSaloon.bookings.forms import BookingForm
from HairSaloon.bookings.models import Booking


# Create your views here.

def bookings_json(request):
    # bookings = [
    #     {
    #         "title": "Haircut with John",
    #         "start": "2024-03-21T13:30:00",
    #         "end": "2024-03-21T14:00:00"
    #     },
    #     {
    #         "title": "Coloring with Jane",
    #         "start": "2024-03-22T12:00:00",
    #         "end": "2024-03-22T13:30:00"
    #     }
    # ]
    # return JsonResponse(bookings, safe=False)
    bookings = Booking.objects.all()
    booking_list = serialize('json', bookings, fields=('service', 'date', 'time'))
    return JsonResponse(booking_list, safe=False)


class BookingView(views.FormView):
    template_name = 'bookings/dashboard.html'
    form_class = BookingForm
    # success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(BookingView, self).get_context_data(**kwargs)
        bookings = Booking.objects.all().prefetch_related()
        context['bookings'] = bookings
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['upcoming_bookings'] = bookings.filter(date__gte=datetime.today())
        context['passed_bookings'] = bookings.filter(date__lte=datetime.today())

        return context

    def get_end_time(self, booking):

        dummy_date = datetime(1, 1, 1)  # Year, month, day
        start_datetime = datetime.combine(dummy_date, booking.start)
        end_datetime = start_datetime + timedelta(minutes=booking.service.duration)

        return end_datetime.time()

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.end = self.get_end_time(booking)

        available_hairdresser = Booking.get_hairdresser(booking)

        if available_hairdresser:
            booking.hairdresser = available_hairdresser[0]
            booking.save()
            messages.success(self.request, 'Your booking has been successfully created.')
            return self.render_to_response(self.get_context_data(form=self.form_class()))
        else:
            # Instead of using form_invalid, manually add an error to the form
            # and re-render the template with the form containing errors.
            form.add_error(None, 'No hairdresser available for the selected date/time.')
            return self.render_to_response(self.get_context_data(form=form))
