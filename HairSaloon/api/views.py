from django.core.serializers import serialize
from django.http import JsonResponse

from HairSaloon.bookings.models import Booking
from HairSaloon.services.models import Service


# Create your views here.

def get_service_duration(request, pk):
    service = Service.objects.get(pk=pk)
    return JsonResponse({'duration': service.duration})


def get_all_bookings(request):
    all_bookings = Booking.objects.all().select_related('service')  # Use select_related to optimize DB queries

    # Construct a list of dictionaries with the required fields
    bookings_data = []
    for booking in all_bookings:
        bookings_data.append({
            'title': booking.service.name,  # Assuming 'name' is a field on your Service model
            'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
            'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
            # Add more fields as necessary
        })

    # Convert the list of dictionaries to JSON
    return JsonResponse(bookings_data, safe=False)
