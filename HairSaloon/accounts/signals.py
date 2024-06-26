from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from HairSaloon.accounts.models import Profile
from HairSaloon.hairdressers.models import HairDresser

# a signal is a function that is triggerd when certain event occurs.
# the model should be manually added in the apps file of the app module
# and append the Config class to have a method ready()


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            HairDresser.objects.get_or_create(user=instance)
        return Profile.objects.create(user=instance)

    if instance.is_superuser:
        return

    if instance.is_staff:
        return HairDresser.objects.get_or_create(user=instance)
    else:
        try:
            HairDresser.objects.get(user=instance).delete()
        except HairDresser.DoesNotExist:
            pass
