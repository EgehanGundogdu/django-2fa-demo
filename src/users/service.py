# users/service.py
from typing import Optional

import pyotp
from django.conf import settings

from users.models import OTPConfiguration, OTPConfigurationStatus


class OTPConfigurationService:
    def get_or_create_otp_configuration(self, user, **kwargs):
        otp_configuration, _ = OTPConfiguration.objects.get_or_create(
            user=user,
            **kwargs,
            defaults={
                "status": OTPConfigurationStatus.INITIALIZATION_STARTED,
                "secret_key": pyotp.random_base32(),
            },
        )

        return otp_configuration

    def get_provisioning_uri(
        self,
        otp_configuration: OTPConfiguration,
        name: str,
        issuer_name: Optional[str] = None,
    ) -> str:
        if not issuer_name:
            issuer_name = settings.APP_NAME
        return otp_configuration.totp.provisioning_uri(
            name=name, issuer_name=issuer_name
        )

    def update_otp_configuration(self, instance, **kwargs):
        kwargs.pop("secret_key", None)
        status = kwargs.get("status", None)

        if status and not instance.status == OTPConfigurationStatus.COMPLETED:
            instance.status = status

        for k, v in kwargs.items():
            setattr(instance, k, v)

        instance.save()
        return instance

    def check_code_is_valid(self, otp_confiuration: OTPConfiguration, code: str):
        return otp_confiuration.totp.verify(code)
