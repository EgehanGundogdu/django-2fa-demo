# users/mixins.py

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin


class OTPSetupSessionKeyRequiredMixin(AccessMixin):
    key = settings.OTP_SETUP_SESSION_USER_PK_KEY

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get(self.key, None):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OTPVerifySessionKeyRequiredMixin(OTPSetupSessionKeyRequiredMixin):
    key = settings.OTP_VERIFY_SESSION_USER_PK_KEY
