from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=11, unique=True, null=False, blank=False)
    rate = models.DecimalField(max_digits=1, decimal_places=1, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_user', default=None, null=True)

    def __str__(self):
        return self.name
