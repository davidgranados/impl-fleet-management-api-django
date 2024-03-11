from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model that support using email instead of username.
    """

    username = None
    email = models.EmailField(_("email address"), max_length=255, unique=True, blank=False, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
