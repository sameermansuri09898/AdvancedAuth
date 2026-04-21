from django.template.defaultfilters import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=10, unique=True)
    
    
    
class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_otp_expired(self):
        return self.otp_created_at + timezone.timedelta(minutes=10) < timezone.now()

    def __str__(self):
        return self.user.username

