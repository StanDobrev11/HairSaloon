from django.urls import path

from HairSaloon.api.views import get_service_duration, get_all_bookings

urlpatterns = [
    path('get-service-duration/<int:pk>/', get_service_duration, name='service duration'),
    path('get-all-bookings/', get_all_bookings, name='all bookings'),
]
