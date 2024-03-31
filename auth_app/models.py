from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from auth_app.commons import (
    default_date_plus_five_min,
    default_date,
    default_pin_code
)


class User(AbstractUser):

    password = models.CharField(
        _("password"),
        max_length=128,
        default=make_password(settings.AUTH_USER_DEFAULT_PASSWORD)
    )

    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
        editable=True
    )
    email = models.EmailField(_("email address"),
                              blank=False,
                              unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Pin(models.Model):
    pin_code = models.CharField(max_length=6, default=default_pin_code)
    created_at = models.DateTimeField(default=default_date)
    use_before = models.DateTimeField(default=default_date_plus_five_min)
    used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.pin_code

    class Meta:
        verbose_name = "Пинкод"
        verbose_name_plural = "Пинкоды"
