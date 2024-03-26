from django.contrib import admin

from .models import HairSaloonUser, Profile


# Define the inline admin panel for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# Register the HairSaloonUser model and include the ProfileInline
@admin.register(HairSaloonUser)
class HairSaloonUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(HairSaloonUserAdmin, self).get_inline_instances(request, obj)
