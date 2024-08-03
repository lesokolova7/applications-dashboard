from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import pyotp

User = get_user_model()


class OTPBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, otp=None, **kwargs):
        user = super().authenticate(
            request, username=username, password=password, **kwargs
        )
        if user and otp:
            totp = pyotp.TOTP(user.otp_secret_key)
            if totp.verify(otp):
                return user
        return None
