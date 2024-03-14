from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    fullname = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(default=18, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    owner = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(f'{self.fullname}_{self.phone_number}')
