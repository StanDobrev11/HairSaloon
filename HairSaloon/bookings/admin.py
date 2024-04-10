from django.contrib import admin

from HairSaloon.bookings.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'hairdresser', 'date', 'start', 'cancelled')
    list_filter = ('cancelled', 'date', 'service', 'hairdresser')
    ordering = ('-date', '-start')
    search_fields = ('user__email', 'service__name', 'hairdresser__user__email')
