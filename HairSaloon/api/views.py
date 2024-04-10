from datetime import date

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404

from HairSaloon.bookings.models import Booking
from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service


# Create your views here.
def load_services(request):
    if request.user.is_authenticated:
        hairdresser_id = request.GET.get('hairdresser_id')
        services = Service.objects.filter(hairdressers__id=hairdresser_id).order_by('name')
        services_data = [{'id': service.id, 'name': service.name} for service in services]
        return JsonResponse(services_data, safe=False)


def get_service_duration(request, pk):
    if request.user.is_authenticated:
        service = get_object_or_404(Service, pk=pk)
        return JsonResponse({'duration': service.duration})

    return redirect('index')


def get_filtered_bookings(request):
    if request.user.is_anonymous:
        return redirect('index')

    current_user = request.user
    bookings = Booking.objects.select_related('service', 'user', 'hairdresser__user').all()

    # Assuming you have a method to get available hairdressers for a service at a given time
    def is_service_available(booking):
        # Implement logic to check if at least one hairdresser is available for the service at the given time
        available_hairdressers = Booking.get_hairdresser(booking)

        return True if available_hairdressers else False

    def format_booking(booking, include_title=True, include_cancelled=True, check_is_hairdresser=False,
                       check_is_owner=False):
        is_hairdresser = booking.hairdresser.user == request.user if check_is_hairdresser else False
        is_owner = booking.user == request.user if check_is_owner else False
        is_available = is_service_available(booking)
        # mapper = map_drop_down_id_to_user_id()
        return {
            'title': booking.service.name if (include_title and (is_owner or current_user.is_superuser)) else '',
            'start': booking.date.strftime("%Y-%m-%dT") + booking.start.strftime("%H:%M:%S"),
            'end': booking.date.strftime("%Y-%m-%dT") + booking.end.strftime("%H:%M:%S"),
            'price': booking.service.price,
            'client': booking.user.full_name,
            'hairdresser': booking.hairdresser.user.full_name,
            'hairdresserId': str(booking.hairdresser.id),
            'notes': booking.notes,
            'isCancelled': booking.cancelled if include_cancelled else None,
            'isHairDresser': is_hairdresser,
            'isOwner': is_owner,
            'isAvailable': is_available,
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


def map_drop_down_id_to_user_id():
    hairdressers = HairDresser.objects.all().order_by('user__first_name', 'user__last_name')
    mapper = {}
    for idx in range(1, hairdressers.count() + 1):
        mapper[hairdressers[idx - 1].id] = str(idx)

    return mapper
