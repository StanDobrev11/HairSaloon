from django.urls import path

from HairSaloon.bookings.views import BookingView, bookings_json

urlpatterns = [
    path('', BookingView.as_view(), name='dashboard'),
    path('api/bookings/', bookings_json, name='bookings_json'),
]
