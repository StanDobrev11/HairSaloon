from django.contrib import admin

from HairSaloon.services.models import Service


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
