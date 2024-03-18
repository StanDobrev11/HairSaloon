from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon.bookings.forms import BookingForm


# Create your views here.

# class DashboardView(views.TemplateView):
#     template_name = 'bookings/dashboard.html'


class BookingView(views.FormView):
    template_name = 'bookings/dashboard.html'
    form_class = BookingForm
    # success_url = reverse_lazy('success_page')
    success_url = HttpResponse('Success')

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # Here, you can handle the booking logic.
    #     booking_date = form.cleaned_data['date']
    #     booking_time = form.cleaned_data['time']
    #     # Logic to create an Appointment object...
    #     return super().form_valid(form)
