from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from HairSaloon.accounts.managers import HairSaloonUserManager


# Create your models here.
class HairSaloonUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    # we have only password and last_login inherited from AbstractBaseUser
    # therefore we need to define username or another credentials

    # check AbstractUser for proper/additional definition of attributes

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    # the idea behind below 3 fields is that the user must have name and number
    # to be contacted in connection with their appointments
    # when in DEBUG, the fileds will be set to optional
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=15, blank=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # is_staff and is_active are required to be used in admin
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    # we need to spec instruct django what will be considered 'username'
    # and AUTH_BASE_MODEL to point to this class in settings.py
    USERNAME_FIELD = 'email'

    # the custom class needs to inherit PermissionsMixin in order to work for auth

    # we need to define custom manager
    # the manager must inherit BaseUserManager in order to change username field to email
    objects = HairSaloonUserManager()
