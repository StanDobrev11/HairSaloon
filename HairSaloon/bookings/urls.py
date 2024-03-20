from django.urls import path

from HairSaloon.bookings.views import BookingView

urlpatterns = [
    path('', BookingView.as_view(), name='dashboard'),
]
