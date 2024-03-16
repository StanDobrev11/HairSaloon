from django.shortcuts import render
from django.views import generic as views


# Create your views here.

class DashboardView(views.ListView):
    template_name = 'accounts/../../templates/bookings/dashboard.html'
