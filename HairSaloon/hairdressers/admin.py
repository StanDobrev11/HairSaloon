from django.contrib import admin

from HairSaloon.hairdressers.models import HairDresser


# Register your models here.
@admin.register(HairDresser)
class HairDresserAdmin(admin.ModelAdmin):
    list_display = ('name',)
