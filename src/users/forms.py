# users/forms.py
from django import forms

from users.service import OTPConfigurationService


class OTPCodeVerifyForm(forms.Form):
    code = forms.CharField(max_length=6, help_text="Enter code after first scan.")

    def clean_code(self):
        code = self.cleaned_data["code"]
        otp_configuration = self.user.otpconfiguration
        service = OTPConfigurationService()
        if service.check_code_is_valid(otp_configuration, code=code):
            return code
        raise forms.ValidationError("Your code is mismatched. Please try again.")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
