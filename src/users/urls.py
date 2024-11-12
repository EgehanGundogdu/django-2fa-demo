from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import SetupTwoFactorAuthView, UserLoginView, UserOTPVerifyView, UserRegisterView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("otp-verify/", UserOTPVerifyView.as_view(), name="otp_verify"),
    path(
        "setup_two_factor_auth/",
        SetupTwoFactorAuthView.as_view(),
        name="setup_two_factor_auth",
    ),
]
