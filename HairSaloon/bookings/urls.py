from django.urls import path

from HairSaloon.bookings.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]