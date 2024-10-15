from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime

# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Keep email unique
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

def get_default_expires_at():
    return timezone.now() + datetime.timedelta(minutes=5)  # Default expiration time for OTPs

# OTP model
class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expires_at)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
