from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):
        return self.username


class Wallet(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    wall_amount = models.FloatField(default=250, null=True, blank=True)

    def __str__(self):
        return str(self.user)
