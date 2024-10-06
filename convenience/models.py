import uuid

from django.db import models
from enum import Enum
from django.utils import timezone


# class TYPE_CONVENIENCE(Enum):
#     PRODUCT = 'PR'
#     POLICY = 'PO'


# Create your models here.
class Convenience(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, null=True, blank=True)
    parent = models.IntegerField(null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(choices=[('EQUIPMENT', 'Equipment'), ('CONVENIENCE', 'Convenience')], max_length=20, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    priority = models.IntegerField(null=True, default=None, blank=True)
    code = models.CharField(max_length=40, null=True, default=None, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
