from django.contrib.auth.models import User
from django.db import models

from convenience.models import Convenience
from location.models import Location


# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11, unique=True, null=False, blank=False)
    rate = models.DecimalField(max_digits=1, decimal_places=1, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization', default=None, null=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True, default=None)
    conveniences = models.ManyToManyField(Convenience, blank=True, null=True, default=None, related_name='organizations')

    objects = models.Manager()

    def __str__(self):
        return self.name
