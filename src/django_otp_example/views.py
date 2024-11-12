from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class OtpVerifiedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user, "is_verified", False)

    def handle_no_permission(self):
        return redirect(reverse_lazy(settings.LOGIN_URL))


class SecretPageView(LoginRequiredMixin, OtpVerifiedRequiredMixin, TemplateView):
    template_name = "core/secret.html"
