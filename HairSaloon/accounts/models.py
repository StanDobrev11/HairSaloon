from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class HairSaloonUser(auth_models.AbstractBaseUser):
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

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # we need to spec instruct django what will be considered 'username'
    # and AUTH_BASE_MODEL to point to this class in settings.py
    USERNAME_FIELD = 'email'

























