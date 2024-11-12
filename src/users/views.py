# users/views.py
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView

from users.forms import OTPCodeVerifyForm
from users.mixins import OTPSetupSessionKeyRequiredMixin, OTPVerifySessionKeyRequiredMixin
from users.models import OTPConfigurationStatus
from users.service import OTPConfigurationService


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("index")
    success_message = _("You are successfuly registered. You can login now.")


class UserLoginView(BaseLoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        user = form.get_user()
        otp_configuration = getattr(user, "otpconfiguration", None)
        if not otp_configuration or otp_configuration.status != OTPConfigurationStatus.COMPLETED:
            self.request.session[settings.OTP_SETUP_SESSION_USER_PK_KEY] = user.pk
            return redirect(reverse_lazy("users:setup_two_factor_auth"))
        else:
            self.request.session[settings.OTP_VERIFY_SESSION_USER_PK_KEY] = user.pk
            return redirect(reverse_lazy("users:otp_verify"))


class UserOTPVerifyView(OTPVerifySessionKeyRequiredMixin, FormView):
    success_url = reverse_lazy("index")
    form_class = OTPCodeVerifyForm
    template_name = "users/otp_verify.html"

    def form_valid(self, form):
        user = self.get_user_with_session_key()
        self.request.session.pop(settings.OTP_VERIFY_SESSION_USER_PK_KEY)
        auth_login(self.request, user)
        self.request.session["is_verified"] = True
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_user_with_session_key()
        return kwargs

    def get_user_with_session_key(self):
        return User.objects.get(pk=self.request.session.get(settings.OTP_VERIFY_SESSION_USER_PK_KEY))


class SetupTwoFactorAuthView(
    OTPSetupSessionKeyRequiredMixin,
    SuccessMessageMixin,
    FormView,
):
    service = OTPConfigurationService()
    form_class = OTPCodeVerifyForm
    template_name = "users/setup_2fa.html"
    success_url = reverse_lazy("index")
    success_message = _("Two-factor authentication has been successfully enabled.")

    def form_valid(self, form):
        user = self.get_user_with_session_key()
        otp_configuration = user.otpconfiguration
        self.service.update_otp_configuration(instance=otp_configuration, status=OTPConfigurationStatus.COMPLETED)
        del self.request.session[settings.OTP_SETUP_SESSION_USER_PK_KEY]
        auth_login(self.request, user)
        self.request.session["is_verified"] = True
        return super().form_valid(form)

    def get_user_with_session_key(self):
        return User.objects.get(pk=self.request.session.get(settings.OTP_SETUP_SESSION_USER_PK_KEY))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user_with_session_key()
        otp_configuration = self.service.get_or_create_otp_configuration(user)
        provisioning_uri = self.service.get_provisioning_uri(otp_configuration, name=user.username)
        context["provisioning_uri"] = provisioning_uri
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_user_with_session_key()
        return kwargs
