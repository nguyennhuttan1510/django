from django.db import models
from enum import Enum
from django.utils import timezone


class TYPE_CONVENIENCE(Enum):
    PRODUCT = 'PR'
    POLICY = 'PO'


# Create your models here.
class Convenience(models.Model):
    TYPE_CONVENIENCE_CHOICES = [
        (TYPE_CONVENIENCE.PRODUCT.value, TYPE_CONVENIENCE.PRODUCT.name),
        (TYPE_CONVENIENCE.POLICY.value, TYPE_CONVENIENCE.POLICY.name)
    ]
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, null=True, blank=True)
    value = models.CharField(max_length=50, default=0)
    parent = models.IntegerField(null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=True)
    type = models.CharField(choices=TYPE_CONVENIENCE_CHOICES, default=TYPE_CONVENIENCE.PRODUCT.value, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
