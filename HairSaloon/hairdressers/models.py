from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from HairSaloon.services.models import Service

UserModel = get_user_model()


class HairDresser(models.Model):
    """
    This model is created via ADMIN site, triggered by a signal when the user is assigned as 'staff'

    The model is used to define the hairdresser working in the salon and
    returns details to the templates.

    It has a relation to the provided services so each hairdresser provides
    all or part of the listed services.

    The photo of the hairdresser should be considered as the account photo.

    When a user is created and the user is a hairdresser, the is_staff should be ticked
    and staff access provided.

    When a new hairdresser is employed, the information below should be completed
    in full
    """

    BACKGROUND_MAX_LENGTH = 500

    background = models.TextField(max_length=500)
    working_since = models.DateField(blank=True, null=True)

    # Provides link to services available and handled by the hairdresser
    services = models.ManyToManyField(
        to=Service,
        related_name='hairdressers'
    )

    # Allows the creation of a HairDresser without associated user
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='hairdresser_profile',
        null=True,
    )

    @property
    def age(self):
        if self.user.profile.date_of_birth:
            today = datetime.today()
            return today.year - self.user.profile.date_of_birth.year - ((today.month, today.day) < (
                self.user.profile.date_of_birth.month, self.user.profile.date_of_birth.day))
        return None

    def __str__(self):
        return self.user.full_name
