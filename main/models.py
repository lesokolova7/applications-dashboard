import pyotp
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    otp_secret_key = models.CharField(max_length=32, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_set", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.otp_secret_key:
            self.otp_secret_key = pyotp.random_base32()
        super().save(*args, **kwargs)
