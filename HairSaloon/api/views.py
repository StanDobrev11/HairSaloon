from datetime import date

from django.core.serializers import serialize
from django.http import JsonResponse

from HairSaloon import bookings
from HairSaloon.bookings.models import Booking
from HairSaloon.bookings.views import BookingView
from HairSaloon.services.models import Service


# Create your views here.

def get_service_duration(request, pk):
    service = Service.objects.get(pk=pk)
    return JsonResponse({'duration': service.duration})


def get_all_bookings(request):
    all_bookings = Booking.objects.prefetch_related()
    current_user = request.user

    result = filter_bookings(all_bookings, current_user, request)

    return JsonResponse(result, safe=False)


def filter_bookings(all_bookings, current_user, request):
    bookings_data = []
    if current_user.is_superuser:
        for booking in all_bookings:
            bookings_data.append({
                'title': booking.service.name,  # Assuming 'name' is a field on your Service model
                'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
                'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
                'price': booking.service.price,
                'client': booking.user.full_name,
                'hairdresser': booking.hairdresser.user.full_name,
                'notes': booking.notes,
            })
    elif current_user.is_staff:
        for booking in all_bookings:
            is_hairdresser = booking.hairdresser == request.user.hairdresser_profile
            bookings_data.append({
                'title': booking.user.full_name if is_hairdresser else '',
                'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
                'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
                'price': booking.service.price,
                'client': booking.user.full_name,
                'notes': booking.notes,
                'hairdresser': booking.hairdresser.user.full_name,
                'isHairDresser': is_hairdresser,
            })
    else:
        for booking in all_bookings.filter(date__gte=date.today()):
            is_owner = booking.user == request.user
            bookings_data.append({
                'title': booking.service.name if is_owner else '',
                'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
                'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
                'price': booking.service.price,
                'hairdresser': booking.hairdresser.user.full_name,
                'notes': booking.notes,
                'isOwner': is_owner,
            })

    return bookings_data
