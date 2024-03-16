from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from HairSaloon.accounts.models import Profile

# a signal is a function that is triggerd when certain event occurs.
# the model should be manually added in the apps file of the app module
# and append the Config class to have a method ready()

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created_signal(sender, instance, created, **kwargs):
    # will be executed on every save when user is created.
    # sender is the class -> UserModel
    # instance is the current user saved in the db
    # created is bool returning True if is newly created and a first save
    if not created:
        return

    Profile.objects.create(user=instance)
