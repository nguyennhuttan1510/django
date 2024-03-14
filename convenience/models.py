from django.db import models

from organization.models import Organization


# Create your models here.
class Convenience(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    parent = models.BigIntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.name
