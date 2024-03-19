from django.contrib import admin

from HairSaloon.bookings.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'start', 'end', 'service',)
