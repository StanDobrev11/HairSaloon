from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon.bookings.forms import BookingForm
from HairSaloon.bookings.models import Booking


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     bookings = Booking.objects.all()
    #     booking_list = serialize('json', bookings)
    #
    #     return JsonResponse(booking_list, safe=False)
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # Here, you can handle the booking logic.
    #     booking_date = form.cleaned_data['date']
    #     booking_time = form.cleaned_data['time']
    #     # Logic to create an Appointment object...
    #     return super().form_valid(form)
