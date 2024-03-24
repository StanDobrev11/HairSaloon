from django.contrib import admin

from HairSaloon.hairdressers.models import HairDresser


# Register your models here.
@admin.register(HairDresser)
class HairDresserAdmin(admin.ModelAdmin):
    list_display = ('display_full_name', 'working_since')

    def display_full_name(self, obj):
        # Check if the hairdresser has an associated user and return the user's full name
        return obj.user.full_name if obj.user else "No associated user"

    display_full_name.short_description = "Full Name"
