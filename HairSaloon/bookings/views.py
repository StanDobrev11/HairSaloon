from datetime import datetime, timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon import bookings
from HairSaloon.bookings.forms import BookingForm
from HairSaloon.bookings.models import Booking
from HairSaloon.services.models import Service


# Create your views here.

# class DashboardView(views.TemplateView):
#     template_name = 'bookings/dashboard.html'
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
    # template_name = 'bookings/calendar.html'
    template_name = 'bookings/dashboard.html'
    form_class = BookingForm
    # success_url = reverse_lazy('success_page')
    success_url = HttpResponse('Success')

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user

        available_hairdresser = Booking.get_hairdresser(booking)

        if available_hairdresser:
            booking.hairdresser = available_hairdresser[0]
            # calculating and saving end time
            booking.end = (booking.start + timedelta(minutes=booking.service.duration)).time()

            booking.save()
            messages.success(self.request, 'Your booking has been successfully created.')
            return super().form_valid(form)
        else:
            # Instead of using form_invalid, manually add an error to the form
            # and re-render the template with the form containing errors.
            form.add_error(None, 'No hairdresser available for the selected date/time.')
            return self.render_to_response(self.get_context_data(form=form))
