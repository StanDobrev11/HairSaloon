from django.contrib import admin

from HairSaloon.services.models import Service


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'male_female_child', 'duration', 'price')
    list_filter = ('male_female_child',)
    search_fields = ('name', 'description',)
