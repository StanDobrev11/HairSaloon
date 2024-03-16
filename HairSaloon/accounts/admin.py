from django.contrib import admin
from django.contrib.auth.models import User

from HairSaloon.accounts.models import HairSaloonUser


# Register your models here.
@admin.register(HairSaloonUser)
class HairSaloonUserAdmin(admin.ModelAdmin):
    pass
