# users/models.py

import pyotp
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class OTPConfigurationStatus(models.TextChoices):
    NOT_INITIALIZED = "not_initialized", _("Not initialized")
    INITIALIZATION_STARTED = "initialization_started", _("Initialization started")
    COMPLETED = "completed", _("Completed")
    FAILED = "failed", _("Failed")


class OTPConfiguration(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=OTPConfigurationStatus.choices,
        default=OTPConfigurationStatus.NOT_INITIALIZED,
    )
    secret_key = models.CharField(max_length=255)

    @property
    def totp(self):
        return pyotp.TOTP(s=self.secret_key)
