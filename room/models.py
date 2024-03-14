from django.contrib.auth.models import User
from django.db import models

from convenience.models import Convenience
from organization.models import Organization


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_room', default=None, null=True)
    conveniences = models.ManyToManyField(Convenience)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
