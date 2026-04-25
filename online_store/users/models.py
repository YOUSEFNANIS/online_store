from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class seller(models.Model):
    store_name = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True)
    user = models.OneToOneField(to=User, on_delete=models.PROTECT)
    profile_image = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    def __str__(self):
        username = self.user.first_name + ' ' + self.user.last_name
        return username
    
class customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.PROTECT)
    profile_image = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    
    def __str__(self):
        username = self.user.first_name + ' ' + self.user.last_name
        return username