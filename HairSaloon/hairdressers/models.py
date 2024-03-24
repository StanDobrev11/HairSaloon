from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from HairSaloon.services.models import Service

UserModel = get_user_model()


class HairDresser(models.Model):
    """
    This model is created via ADMIN site.

    The model is used to define the hairdresser working in the salon and
    return details to the templates.
    It has a relation to the provided services so each hairdresser provides
    all or part of the listed services.
    The photo of the hairdresser should be considered as the account photo.
    When a user is created and the user is a hairdresser, the is_staff should be ticked
    and staff access provided.
    The user and hairdresser models linked.
    When a new hairdresser is employed, the information below should be completed
    in full
    """

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    BACKGROUND_MAX_LENGTH = 500
    GENDER_MAX_LENGTH = 6
    NAME_MAX_LENGTH = 150
    PHOTO_UPLOAD_DIR = 'hairdressers/'

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    date_of_birth = models.DateField(blank=True, null=True)
    background = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    working_since = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=PHOTO_UPLOAD_DIR, blank=True, null=True)

    # Provides link to services available and handled by the hairdresser
    services = models.ManyToManyField(
        to=Service,
        related_name='hairdressers'
    )

    # Allows the creation of a HairDresser without an associated user
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='hairdresser_profile',
        null=True,
    )

    @property
    def age(self):
        return datetime.today().year - self.date_of_birth.year

    def __str__(self):
        return self.name
