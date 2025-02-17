from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.code}"