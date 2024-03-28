from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from HairSaloon.bookings.models import Booking
from HairSaloon.services.models import Service


# Create your views here.

def get_service_duration(request, pk):

    if request.user.is_authenticated:
        service = Service.objects.get(pk=pk)
        return JsonResponse({'duration': service.duration})

    return redirect('index')


def get_filtered_bookings(request):
    if request.user.is_anonymous:
        return redirect('index')

    current_user = request.user
    bookings = Booking.objects.select_related('service', 'user', 'hairdresser__user').all()

    def format_booking(booking, include_title=True, include_cancelled=True, check_is_hairdresser=False,
                       check_is_owner=False):
        is_hairdresser = booking.hairdresser.user == request.user if check_is_hairdresser else False
        is_owner = booking.user == request.user if check_is_owner else False
        return {
            'title': booking.service.name if (include_title and (is_owner or current_user.is_superuser)) else '',
            'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
            'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
            'price': booking.service.price,
            'client': booking.user.full_name,
            'hairdresser': booking.hairdresser.user.full_name,
            'notes': booking.notes,
            'isCancelled': booking.cancelled if include_cancelled else None,
            'isHairDresser': is_hairdresser,
            'isOwner': is_owner,
        }

    if current_user.is_superuser:
        # For superuser, include all details
        bookings_data = [format_booking(booking) for booking in bookings]
    elif current_user.is_staff:
        # For staff, conditionally include title and cancelled status
        bookings_data = [format_booking(booking, check_is_hairdresser=True) for booking in bookings]
    elif current_user.is_authenticated:
        # For other users, filter by pending and conditionally include title
        bookings_data = [format_booking(booking, include_title=False, include_cancelled=False, check_is_owner=True) for
                         booking in bookings.filter(date__gte=date.today()).exclude(cancelled=True)]

    return JsonResponse(bookings_data, safe=False)
